import sys
import httpx

if __name__ == "__main__":
    question = "Who plays Arya Stark?"
    if len(sys.argv) > 1:
        question = sys.argv[1]

    httpx.get(f"http://localhost:8000/game-of-thrones-query?question={question}")
