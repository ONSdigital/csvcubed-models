import asyncio
import math


async def run_task(i: int) -> None:
    print(f"Starting Task {i}")
    await asyncio.sleep(1)
    print(f"Finishing Task {i}")
    return int(math.pow(i, 2))


async def main():
    tasks_to_await = [
        run_task(i) for i in range(0, 20)
    ]

    # Is we do them in series, we have to wait 20 seconds for the app to finish
    # and it starts and finishes each task before going on to the next one.
    # for task in tasks_to_await:
    #     await task

    # If we do them in parallel we wait 1 second for the app to finish
    # and it starts all of the tasks at roughly the same time.
    results = await asyncio.gather(*tasks_to_await, return_exceptions=True)
    joined_values = ", ".join([str(sq) for sq in results])
    print(f"The squares are {joined_values}")


if __name__ == "__main__":
    asyncio.run(main())
