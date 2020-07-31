from collections import deque, namedtuple


class Queues:
    def __init__(self):
        self.change_oil_queue = deque()
        self.inflate_tires_queue = deque()
        self.diagnostic_queue = deque()
        self.last_ticket_number = 0
        self.next_ticket = None
        QueueInfo = namedtuple('QueueInfo', 'name, queue, time')
        self.QUEUES = (
            QueueInfo("change_oil", self.change_oil_queue, 2),
            QueueInfo("inflate_tires", self.inflate_tires_queue, 5),
            QueueInfo("diagnostic", self.diagnostic_queue, 30),
        )

    def get_estimated_time(self, chosen_service_time):
        time = 0
        for queue_info in self.QUEUES:
            if queue_info.time <= chosen_service_time:
                time += len(queue_info.queue) * queue_info.time
        return time

    def get_queues_length(self):
        return {queue_info.name: len(queue_info.queue) for queue_info in self.QUEUES}

    def set_next_ticket(self):
        waiting_queue_times = [queue_info.time for queue_info in self.QUEUES if len(queue_info.queue) > 0]
        if len(waiting_queue_times) == 0:
            return None

        shortest_time = min(waiting_queue_times)
        next_queue = None
        for queue_info in self.QUEUES:
            if queue_info.time == shortest_time:
                next_queue = queue_info.queue
                break
        assert next_queue is not None and len(next_queue) > 0

        next_ticket = next_queue.popleft()
        self.next_ticket = next_ticket

    def get_by_name(self, queue_name):
        service_queue_info = None
        for queue_info in self.QUEUES:
            if queue_info.name == queue_name:
                service_queue_info = queue_info
        return service_queue_info
