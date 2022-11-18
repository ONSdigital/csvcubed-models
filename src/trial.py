from typing import Callable, Any, List
from dataclasses import dataclass
import math
import asyncio 
import concurrent.futures

def _expensively_square_number(item: int) -> int:
    print(f"Beginning expensive query {item}")

    for i in range(0, 4000000):
        math.sqrt(i)

    print(f"Ending expensive query {item}")
    return int(math.pow(item, 2))

def _return_number(number: int) -> int:
    return number + 1

async def main():
    my_favourite_items = []

    things_to_do = [
        CpuBoundTask(_expensively_square_number, [i]) for i in range(0, 20)
    ]

    my_new_favourite_items = await run_cpu_bound_tasks_concurrently(things_to_do)
    
    print(f"These are my items: {my_favourite_items}")
    print(f"These are my new items: {my_new_favourite_items}")


@dataclass
class CpuBoundTask:
    function_to_call: Callable
    arguments: List[Any]

async def run_cpu_bound_tasks_concurrently(things_to_run: List[CpuBoundTask]) -> List[Any]:
    loop = asyncio.get_running_loop()

    with concurrent.futures.ThreadPoolExecutor() as pool:
        tasks_to_await = [ loop.run_in_executor(pool, thing.function_to_call, *thing.arguments) for thing in things_to_run ]
        return await asyncio.gather(*tasks_to_await)


if __name__=="__main__":
    asyncio.run(main())