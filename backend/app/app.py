from fastapi import FastAPI
import endpoints


def create_app():
    app = FastAPI()
    app.include_router(endpoints.router, prefix="/endpoints")

    @app.get("/ping", status_code=200)
    def ping():
        return "I AM OK!"

    return app


app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8081)
