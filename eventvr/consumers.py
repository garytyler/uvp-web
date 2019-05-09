import time
from channels.generic.websocket import JsonWebsocketConsumer


class PlayerConsumer(JsonWebsocketConsumer):
    groups = []
    view = {"gn_euler": {"alpha": 10, "beta": 20, "gamma": 30}}

    def incr_view(self):
        self.view["gn_euler"]["alpha"] += 1
        self.view["gn_euler"]["beta"] += 1
        self.view["gn_euler"]["gamma"] += 1

    def connect(self):
        self.accept()
        self.send_json(self.view)

    def receive_json(self, event=None):
        start = time.time()
        self.send_json(self.view)
        print("Elapsed time {}.".format(time.time() - start))
        self.incr_view()

    def disconnect(self, close_code):
        pass


class QueueConsumer(JsonWebsocketConsumer):
    groups = []

    def connect(self):
        self.accept()
        self.userid = self.scope["url_route"]["kwargs"]["userid"]

    def receive_json(self, content=None):
        self.send_json({"Hello world!"})
        # start = time.time()
        # self.send_json(self.view)
        # print("Elapsed time {}.".format(time.time() - start))
        # self.incr_view()

    def disconnect(self, close_code):
        pass
