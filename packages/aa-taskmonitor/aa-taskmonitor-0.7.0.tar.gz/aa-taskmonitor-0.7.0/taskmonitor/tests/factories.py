import datetime as dt
import itertools
from dataclasses import asdict, dataclass
from random import choice, choices, randint, shuffle
from uuid import UUID

import factory
import factory.fuzzy
from factory.faker import faker

from django.utils import timezone

from taskmonitor.models import TaskLog

# generate fake apps and task names
faker = faker.Faker()
fake_tasks = {}
for app_name in {faker.first_name().lower() for _ in range(24)}:
    fake_tasks[app_name] = [
        app_name + ".tasks." + "_".join(faker.words(3)).lower()
        for _ in range(randint(3, 20))
    ]
fake_tasks_all = list(
    itertools.chain(*[fake_tasks[app_name] for app_name in fake_tasks])
)

fake_words = [obj.lower() for obj in faker.words(50)]
fake_numbers = [randint(0, 1_000_000) for _ in range(100)]
fake_args = fake_words + fake_numbers
shuffle(fake_args)


class TaskLogFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = TaskLog

    app_name = factory.fuzzy.FuzzyChoice(fake_tasks.keys())
    received = factory.fuzzy.FuzzyDateTime(timezone.now() - dt.timedelta(hours=3))
    started = factory.LazyAttribute(
        lambda o: factory.fuzzy.FuzzyDateTime(start_dt=o.received).fuzz()
    )
    task_name = factory.LazyAttribute(lambda o: choice(fake_tasks[o.app_name]))

    @factory.lazy_attribute
    def task_id(self):
        return UUID(faker.uuid4())

    @factory.lazy_attribute
    def args(self):
        return list(choices(fake_args, k=randint(0, 10)))

    @factory.lazy_attribute
    def kwargs(self):
        keys = choices(fake_words, k=randint(0, 20))
        return {key: randint(0, 1_000_000) for key in keys}

    @factory.lazy_attribute
    def runtime(self):
        return (self.timestamp - self.started).total_seconds()

    @factory.lazy_attribute
    def priority(self):
        return choices(
            population=[1, 2, 3, 4, 5, 6, 7, 8, 9],
            weights=[5, 5, 10, 20, 100, 20, 10, 5, 5],
        )[0]

    @factory.lazy_attribute
    def retries(self):
        return choices(
            population=[0, 1, 2, 3],
            weights=[80, 10, 5, 5],
        )[0]

    @factory.lazy_attribute
    def state(self):
        return choices(
            population=[
                TaskLog.State.SUCCESS,
                TaskLog.State.RETRY,
                TaskLog.State.FAILURE,
            ],
            weights=[80, 15, 5],
        )[0]

    @factory.lazy_attribute
    def exception(self):
        if self.state == TaskLog.State.SUCCESS:
            return ""
        return faker.sentence()

    @factory.lazy_attribute
    def traceback(self):
        if self.state == TaskLog.State.SUCCESS:
            return ""
        return faker.paragraph()

    @factory.lazy_attribute
    def timestamp(self):
        max_duration = choices(
            population=[0.5, 1, 10, 30, 120],
            weights=[75, 10, 5, 5, 5],
        )[0]
        start_dt = self.started + dt.timedelta(seconds=0.1)
        return factory.fuzzy.FuzzyDateTime(
            start_dt=start_dt,
            end_dt=start_dt + dt.timedelta(seconds=max_duration),
        ).fuzz()

    @factory.lazy_attribute
    def result(self):
        if self.state == TaskLog.State.SUCCESS:
            return choice(fake_args)
        return None


@dataclass
class ContextStub:
    id: str
    retries: int
    delivery_info: dict
    args: list
    kwargs: dict
    parent_id: str = None

    def asdict(self) -> dict:
        return asdict(self)

    @classmethod
    def create_from_obj(cls, obj: TaskLog):
        return cls(
            parent_id=obj.parent_id,
            retries=obj.retries,
            id=str(obj.task_id),
            delivery_info={
                "is_eager": False,
                "exchange": None,
                "routing_key": None,
                "priority": obj.priority,
            },
            args=obj.args,
            kwargs=obj.kwargs,
        )


@dataclass
class SenderStub:
    name: str
    request: ContextStub
    priority: int

    @classmethod
    def create_from_obj(cls, obj: TaskLog):
        request = ContextStub.create_from_obj(obj)
        return cls(name=obj.task_name, request=request, priority=5)


class QueuedTaskRawFactory(factory.DictFactory):
    body = (
        "W1tdLCB7fSwgeyJjYWxsYmFja3MiOiBudWxsLCAiZXJyYmFja3MiOi"
        "BudWxsLCAiY2hhaW4iOiBudWxsLCAiY2hvcmQiOiBudWxsfV0="
    )
    content_encoding = "utf-8"
    content_type = "application/json"
    headers = factory.Dict(
        {
            "lang": "py",
            "task": factory.LazyAttribute(lambda o: choice(fake_tasks_all)),
            "id": factory.Faker("uuid4"),
            "retries": 0,
            "origin": "dummy@QueuedTaskRawFactory",
            "root_id": None,
            "parent_id": factory.LazyAttribute(lambda o: o.id),
        }
    )
    properties = factory.Dict({"priority": factory.fuzzy.FuzzyInteger(0, 9)})

    class Meta:
        rename = {
            "content_encoding": "content-encoding",
            "content_type": "content-type",
        }

    #     {
    #         "body": "W1tdLCB7fSwgeyJjYWxsYmFja3MiOiBudWxsLCAiZXJyYmFja3MiOiBudWxsLCAiY2hhaW4iOiBudWxsLCAiY2hvcmQiOiBudWxsfV0=",
    #         "content-encoding": "utf-8",
    #         "content-type": "application/json",
    #         "headers": {
    #             "lang": "py",
    #             "task": "taskmonitor.tasks.run_housekeeping",
    #             "id": "7b2416f0-1ff5-4c77-8403-8aafac05b298",
    #             "shadow": None,
    #             "eta": None,
    #             "expires": None,
    #             "group": None,
    #             "group_index": None,
    #             "retries": 0,
    #             "timelimit": [None, None],
    #             "root_id": "7b2416f0-1ff5-4c77-8403-8aafac05b298",
    #             "parent_id": None,
    #             "argsrepr": "()",
    #             "kwargsrepr": "{}",
    #             "origin": "gen9996@bji74-PC",
    #             "ignore_result": False,
    #         },
    #         "properties": {
    #             "correlation_id": "7b2416f0-1ff5-4c77-8403-8aafac05b298",
    #             "reply_to": "853ed4b4-2c52-32cd-be57-4086564ac31e",
    #             "delivery_mode": 2,
    #             "delivery_info": {"exchange": "", "routing_key": "celery"},
    #             "priority": 0,
    #             "body_encoding": "base64",
    #             "delivery_tag": "84f0b41d-c8fc-4dab-88e8-a89afddb1deb",
    #         },
    #     }
    # ]
