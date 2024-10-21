from concurrent.futures import ThreadPoolExecutor


def __handle_exceptions(future):
    try:
        return future.result()
    except Exception as e:

        print(f"Error occurred: {e}")
        return None

def applyInParallelWithErrorHandling(func, items):
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(func, item) for item in items]
        results = [__handle_exceptions(future) for future in futures]
    return results
