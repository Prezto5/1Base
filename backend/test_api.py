import httpx

if __name__ == "__main__":
    try:
        r = httpx.get("http://127.0.0.1:8000/api/v1/products")
        print(r.status_code)
        print(r.text)
    except Exception as e:
        import traceback
        traceback.print_exc() 