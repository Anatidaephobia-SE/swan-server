from .models import TaskType, Tasks, TaskState
from post.models import Post
import json
class Scheduler():
    def schedule(self, post, social_media, task_type : TaskType, schedule_date):
        body = None
        if task_type == TaskType.Twitter:
            body = self.build_twitter_post_body(post, social_media)
        
        if body:
            Tasks.objects.create(task_type=int(task_type), body=body, scheduled_date=schedule_date, state=TaskState.Active)
            return True
        else:
            return False

    def build_twitter_post_body(self, post, social_media):
        data = {}
        data["post_id"] = post.id
        data["social_id"] = social_media.id
        data["type"] = int(TaskType.Twitter)
        return json.dumps(data)