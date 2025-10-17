import math
from collections import defaultdict, Counter


def read_labeled_corpus(train_file):
    sentences = []
    tags = set()
    with open(train_file, "r", encoding="utf-8") as f:
        for line in f:
            words_tags = line.strip().split()
            sentence = []
            for wt in words_tags:
                if "_" not in wt:
                    continue
                word, tag = wt.rsplit("_", 1)
                sentence.append((word, tag))
                tags.add(tag)
            sentences.append(sentence)
    return sentences, sorted(tags)


def create_transition_matrix(alpha, tag_counts, transition_counts, tag_set):
    trans_probs = defaultdict(dict)
    for prev in tag_set:
        total = sum(transition_counts[prev].values())
        for curr in tag_set:
            prob = (transition_counts[prev][curr] + alpha) / (
                total + alpha * len(tag_set)
            )
            trans_probs[prev][curr] = prob
    return trans_probs


def create_emission_matrix(alpha, tag_counts, emission_counts, vocab, tag_set):
    emit_probs = defaultdict(dict)
    for tag in tag_set:
        total = sum(emission_counts[tag].values())
        for word in vocab:
            prob = (emission_counts[tag][word] + alpha) / (total + alpha * len(vocab))
            emit_probs[tag][word] = prob
        emit_probs[tag]["<UNK>"] = alpha / (total + alpha * len(vocab))
    return emit_probs


def assign_unk(word):
    # Suffix-based heuristic: assign tag based on suffix (basic example)
    if word.endswith("ing"):
        return "VBG"
    if word.endswith("ed"):
        return "VBD"
    if word.endswith("ly"):
        return "RB"
    if word.istitle():
        return "NNP"
    return "NN"


def train_hmm(sentences, tags, alpha=1.0):
    tag_counts = Counter()
    transition_counts = defaultdict(Counter)
    emission_counts = defaultdict(Counter)
    start_tag = "<s>"
    stop_tag = "</s>"
    vocab = set()

    for sent in sentences:
        prev = start_tag
        tag_counts[prev] += 1
        for word, tag in sent:
            tag_counts[tag] += 1
            vocab.add(word)
            transition_counts[prev][tag] += 1
            emission_counts[tag][word] += 1
            prev = tag
        transition_counts[prev][stop_tag] += 1
        tag_counts[stop_tag] += 1

    tag_set = tags + [start_tag, stop_tag]
    trans_probs = create_transition_matrix(
        alpha, tag_counts, transition_counts, tag_set
    )
    emit_probs = create_emission_matrix(
        alpha, tag_counts, emission_counts, vocab, tag_set
    )
    return trans_probs, emit_probs, vocab, tag_set


def viterbi(words, trans_probs, emit_probs, tags, vocab):
    T = len(words)
    start_tag = "<s>"
    stop_tag = "</s>"
    V = [{}]
    back = [{}]

    # Initialize
    for tag in tags:
        trans_p = trans_probs[start_tag].get(tag, 1e-10)
        emit_p = emit_probs[tag].get(words[0], emit_probs[tag]["<UNK>"])
        if words[0] not in vocab:
            tag_guess = assign_unk(words[0])
            emit_p = 1.0 if tag == tag_guess else 1e-6
        V[0][tag] = math.log(trans_p) + math.log(emit_p)
        back[0][tag] = start_tag

    # Forward
    for t in range(1, T):
        V.append({})
        back.append({})
        for curr_tag in tags:
            max_prob, prev_tag = float("-inf"), None
            emit_p = emit_probs[curr_tag].get(words[t], emit_probs[curr_tag]["<UNK>"])
            if words[t] not in vocab:
                tag_guess = assign_unk(words[t])
                emit_p = 1.0 if curr_tag == tag_guess else 1e-6
            for pt in tags:
                prob = (
                    V[t - 1][pt]
                    + math.log(trans_probs[pt].get(curr_tag, 1e-10))
                    + math.log(emit_p)
                )
                if prob > max_prob:
                    max_prob = prob
                    prev_tag = pt
            V[t][curr_tag] = max_prob
            back[t][curr_tag] = prev_tag

    # Backtrack
    max_prob, last_tag = float("-inf"), None
    for tag in tags:
        prob = V[T - 1][tag] + math.log(trans_probs[tag].get(stop_tag, 1e-10))
        if prob > max_prob:
            max_prob = prob
            last_tag = tag

    best_path = [last_tag]
    for t in range(T - 1, 0, -1):
        best_path.append(back[t][best_path[-1]])
    best_path.reverse()
    return list(zip(words, best_path))


def tag_file(train_path, test_path, output_path, alpha=1.0):
    sentences, tags = read_labeled_corpus(train_path)
    trans_probs, emit_probs, vocab, tag_set = train_hmm(sentences, tags, alpha)
    use_tags = [t for t in tag_set if t not in ("<s>", "</s>")]

    with open(test_path, "r", encoding="utf-8") as test_file, open(
        output_path, "w", encoding="utf-8"
    ) as out_file:
        for line in test_file:
            words = line.strip().split()
            if not words:  # Skip empty lines
                out_file.write("\n")
                continue
            tagged = viterbi(words, trans_probs, emit_probs, use_tags, vocab)
            output = " ".join([f"{word}_{tag}" for word, tag in tagged])
            out_file.write(output + "\n")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Improved POS Tagging with Viterbi Algorithm"
    )
    parser.add_argument("--train", required=True, help="Path to training file")
    parser.add_argument("--test", required=True, help="Path to test file")
    parser.add_argument("--output", required=True, help="Output file path")
    parser.add_argument(
        "--alpha", type=float, default=1.0, help="Laplace smoothing parameter"
    )
    args = parser.parse_args()

    tag_file(args.train, args.test, args.output, alpha=args.alpha)
