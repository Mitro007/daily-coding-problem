import collections

from str.aho_corasick import AhoCorasickAutomaton


class TestAhoCorasickAutomaton:
    def test_aho_corasick_automaton(self):
        ac = AhoCorasickAutomaton(["vine", "vincent", "cent", "center"])
        assert ac.root is not None
        assert ac.root.word is None
        assert ac.root.failure is None
        assert ac.root.output is None

        for prefix in ["c", "ce", "cen", "cente", "v", "vi", "vin"]:
            node = ac.find(prefix)
            assert node.word is None
            assert node.failure is ac.root
            assert node.output is None

        for prefix in ["cent", "center", "vine"]:
            node = ac.find(prefix)
            assert node.word is prefix
            assert node.failure is ac.root
            assert node.output is None

        vinc = ac.find("vinc")
        assert vinc.word is None
        assert vinc.failure is ac.find("c")
        assert vinc.output is None

        vince = ac.find("vince")
        assert vince.word is None
        assert vince.failure is ac.find("ce")
        assert vince.output is None

        vincen = ac.find("vincen")
        assert vincen.word is None
        assert vincen.failure is ac.find("cen")
        assert vincen.output is None

        vincent = ac.find("vincent")
        assert vincent.word == "vincent"
        assert vincent.failure is ac.find("cent")
        assert vincent.output is ac.find("cent")

        assert ac.find("centre") is None

    def test_get_indices(self):
        words = ["cat", "dog"]
        ac = AhoCorasickAutomaton(words)

        node: AhoCorasickAutomaton.Node = ac.root
        i = 0
        s = "dogcatcatcodecatdog"
        f = [-1] * len(s)
        m = len(words[0])
        while i < len(s) and node:
            if s[i] in node.children:
                node = node.children[s[i]]
                i += 1
            elif node.failure:
                node = node.failure
            else:
                node = ac.root
                i += 1

            if node.word:
                f[i - m] = node.val[0]

        indices = collections.defaultdict(list)
        for w, i in list(map(lambda y: (words[y[1]], y[0]), filter(lambda x: x[1] >= 0, enumerate(f)))):
            indices[w].append(i)
        assert indices == {"dog": [0, 16], "cat": [3, 6, 13]}
