from .CollectorBase import CollectorBase

class CollectPRs(CollectorBase):
    def execute(self, data: dict, metrics: dict, members) -> dict:
        pull_requests = data['pull_requests']
        total = 0
        merged = 0
        closed = 0
        for _,pull_request in pull_requests.items():
            total += 1
            if pull_request['merged'] != False: 
                merged += 1
            elif pull_request['state'] == 'closed': # Quan merged, state es 'closed'
                closed += 1
        metrics['pull_requests'] = {
            'merged': merged,
            'closed': closed,
            'total': total
        }
        return metrics