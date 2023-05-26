import asyncio

# async def async_func1():
#     # 비동기 
#     print("Hello")

# asyncio.run(async_func1())

# 비동기 함수에서 await을 안 쓸 경우 에러 발생
# 코루틴을 잘 처리하기 위해서는 스케줄러가 필요한데 이를 이벤트 루프라고 부름.
# 코루틴을 처리하기 전에 먼저 이벤트 루프를 만들고 처리가 끝나면 이벤트 루프를 닫아야 함.
# 이러한 역할을 간단히 처리해주는 것이 asyncio 모듈의 run 함수임.

# ---

async def async_func1():
    print("Hello")

loop = asyncio.get_event_loop()
loop.run_until_complete(async_func1())
loop.close()

# 이벤트 루프를 실행시킨 뒤, 코루틴 객체가 완료될 때까지 실행해서 이벤트 루프를 닫는 코드입니다.
# 카페에서 아메리카노와 라떼 주문을 받는 것을 asyncio를 사용하여 코드화 한다면,

# --- 

async def make_americano():
    print("Americano Start")
    await asyncio.sleep(3)
    print("Americano End")

async def make_latte():
    print("Latte Start")
    await asyncio.sleep(5)
    print("Latte End")

async def main():
    coro1 = make_americano()
    coro2 = make_latte()
    await asyncio.gather(
        coro1,
        coro2,
    )

print("Main Start")
asyncio.run(main())
print("Main End")

