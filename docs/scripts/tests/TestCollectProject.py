import unittest
from metricsCollectors.CollectProject import CollectProject

class TestCollectProject(unittest.TestCase):

    def setUp(self):

        self.metrics = {}
        self.members = ['member1', 'member2'] 
        self.collector = CollectProject()

    def test_general_projects(self):

        data = {
            "project": {
            "1": {"title": "t1","assignee": None,"status": "Todo","item_type": "Issue"},
            "2": {"title": "t2","assignee": "member1","status": "In Progress","item_type": "DraftIssue"},
            "3": {"title": "t3","assignee": "member1","status": "Todo","item_type": "DraftIssue"},
            "4": {"title": "t4","assignee": "member2","status": "Done","item_type": "Issue"},
            }
        }

        result = self.collector.execute(data, self.metrics, self.members)
        
        expected_result = {
            "project": {
                "assigned_per_member": {
                    "member1": 2,
                    "member2": 1,
                    "non_assigned": 1
                },
                "in_progress_per_member": {
                    "member1": 1,
                    "member2": 0
                },
                "done_per_member": {
                    "member1": 0,
                    "member2": 1
                },
                "in_progress": 1,
                "done": 1,
                "total": 4
            },
        }
        
        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()