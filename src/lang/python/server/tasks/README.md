# Background Tasks

This directory is for organizing background tasks using FastAPI's built-in `BackgroundTasks`.

## Basic Usage

```python
from fastapi import BackgroundTasks

async def write_log(message: str):
    with open("log.txt", "a") as f:
        f.write(message)

@router.post("/send-notification")
async def send_notification(
    background_tasks: BackgroundTasks
):
    background_tasks.add_task(write_log, "Message sent")
    return {"message": "Notification sent"}
```

## Task Organization

Organize tasks by domain in separate files:

```python
# tasks/email.py
class EmailTasks:
    def __init__(self, email_service):
        self.email_service = email_service

    async def send_welcome_email(self, user_email: str):
        await self.email_service.send_email(
            to_email=user_email,
            subject="Welcome!",
            body="Welcome to our service"
        )

# routes/auth.py
@router.post("/register")
async def register(
    user_data: UserCreate,
    background_tasks: BackgroundTasks,
    email_tasks: EmailTasks = Depends(get_email_tasks)
):
    # Create user...
    background_tasks.add_task(
        email_tasks.send_welcome_email,
        user_data.email
    )
    return {"message": "User registered"}
```

## Common Use Cases

- Sending emails
- Processing uploads
- Cleanup operations
- Notifications
- Logging
- Data processing

## Best Practices

1. Keep tasks lightweight
2. Handle errors within tasks
3. Include proper logging
4. Don't rely on return values (they're ignored)
5. Use dependency injection for services

## When to Use Something Else

BackgroundTasks are great for simple async operations, but consider alternatives when you need:
- Long-running tasks (use Celery)
- Scheduled jobs (use APScheduler or Celery Beat)
- Complex task queues (use Redis Queue or Celery)
- Task status monitoring
- Task retries

## Resources

- [FastAPI BackgroundTasks Documentation](https://fastapi.tiangolo.com/tutorial/background-tasks/)
- [Starlette Background Tasks](https://www.starlette.io/background/)
- [FastAPI Tasks Dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-with-yield/)
