from locust import HttpUser, TaskSet, task, between

class WebsiteUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def get_products(self):
        self.client.get("/api/products")

    @task(1)
    def health_check(self):
        self.client.get("/api/health")