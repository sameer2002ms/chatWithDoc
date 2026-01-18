from typing import List, Dict


class DummyAnswerGenerator:
    """
    Debug-only answer generator.
    Returns retrieved chunks as the answer.
    """

    @staticmethod
    def generate(chunks: List[Dict]) -> Dict:
        return {
            "answer": "Relevant sections found in the document:",
            "sources": [
                {
                    "chunk_index": c["chunk_index"],
                    "text": c["text"],
                    "score": c.get("score"),
                }
                for c in chunks
            ],
        }


#for testing purposes only
#for testing purposes only
#for testing purposes only
#for testing purposes only
#for testing purposes only
#for testing purposes only
#for testing purposes only