from .models import TaskType, Tasks, TaskState
from post.models import Post
import json
class Scheduler():
    def schedule_post(self, post, social_media, task_type : TaskType, schedule_date):
        body = None
        if task_type == TaskType.Twitter:
            body = self.build_twitter_post_body(post, social_media)
        #update scheduled date if this post exists
        if Tasks.objects.filter(post=post, task_type=task_type).exists():
            task = Tasks.objects.get(post=post, task_type=task_type)
            task.scheduled_date = schedule_date
            task.save()
            return True
        if body:
            Tasks.objects.create(task_type=int(task_type), post=post, body=body, scheduled_date=schedule_date, state=TaskState.Active)
            return True
        else:
            return False
    def get_post_scheduled_date(self, post, task_type: TaskType):
        if Tasks.objects.filter(post=post, task_type=task_type).exists():
            task = Tasks.objects.get(post=post, task_type=task_type)
            return task.scheduled_date
        return None

    def build_twitter_post_body(self, post, social_media):
        data = {}
        data["post_id"] = post.id
        data["social_id"] = social_media.id
        data["type"] = int(TaskType.Twitter)
        return json.dumps(data)