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
            "1": {"title": "t1","assignee": None,"status": "Todo","item_type": "Issue","iteration":"Iteration 1","issue_type": "Task"},
            "2": {"title": "t2","assignee": "member1","status": "In Progress","item_type": "Issue","iteration":"Iteration 2","issue_type": "Task"},
            "3": {"title": "t3","assignee": "member1","status": "Todo","item_type": "DraftIssue","iteration":None},
            "4": {"title": "t4","assignee": "member2","status": "Done","item_type": "Issue","iteration":None,"issue_type": None},
            },
            "iterations": [
            {"id": "1","title": "Iteration 1","startDate": "2025-02-1","duration": 14},
            {"id": "2","title": "Iteration 2","startDate": "2025-02-15","duration": 14},
            ]
        }
        result = self.collector.execute(data, self.metrics, self.members)
        print(result)
        expected_result = {
            "project": {
                "has_iterations" : True,
                "iterations": {
                    "Iteration 1" : {"title": "Iteration 1","startDate": "2025-02-1","endDate":"2025-02-14","duration": 14},
                    "Iteration 2" : {"title": "Iteration 2","startDate": "2025-02-15","endDate":"2025-02-28","duration": 14},
                },
                "metrics_by_iteration": {
                    "Iteration 1": {
                        "assigned_per_member": {
                            "member1": 0,
                            "member2": 0,
                            "non_assigned": 1
                        },
                        "in_progress_per_member": {
                            "member1": 0,
                            "member2": 0
                        },
                        "done_per_member": {
                            "member1": 0,
                            "member2": 0
                        },
                        "in_progress": 0,
                        "done": 0,
                        "total_issues": 1,
                        "total_issues_with_type": 1,
                        "total_features": 0,
                        "total_tasks": 1,
                        "total_bugs": 0,
                        "total_features_done": 0,
                        "total_features_in_progress": 0,
                        "total": 1
                    },
                    "Iteration 2": {
                        "assigned_per_member": {
                            "member1": 1,
                            "member2": 0,
                            "non_assigned": 0
                        },
                        "in_progress_per_member": {
                            "member1": 1,
                            "member2": 0
                        },
                        "done_per_member": {
                            "member1": 0,
                            "member2": 0
                        },
                        "in_progress": 1,
                        "done": 0,
                        "total_issues": 1,
                        "total_issues_with_type": 1,
                        "total_features": 0,
                        "total_tasks": 1,
                        "total_bugs": 0,
                        "total_features_done": 0,
                        "total_features_in_progress": 0,
                        "total": 1
                    },
                    "no_iteration": {
                        "assigned_per_member": {
                            "member1": 0,
                            "member2": 0,
                            "non_assigned": 0
                        },
                        "in_progress_per_member": {
                            "member1": 0,
                            "member2": 0
                        },
                        "done_per_member": {
                            "member1": 0,
                            "member2": 0
                        },
                        "in_progress": 0,
                        "done": 1,
                        "total_issues": 1,
                        "total_issues_with_type": 0,
                        "total_features": 0,
                        "total_tasks": 0,
                        "total_bugs": 0,
                        "total_features_done": 0,
                        "total_features_in_progress": 0,
                        "total": 2
                    },
                    "total": {
                        "assigned_per_member": {
                            "member1": 1,
                            "member2": 0,
                            "non_assigned": 1
                        },
                        "in_progress_per_member": {
                            "member1": 1,
                            "member2": 0
                        },
                        "done_per_member": {
                            "member1": 0,
                            "member2": 0
                        },
                        "in_progress": 1,
                        "done": 1,
                        "total_issues": 3,
                        "total_issues_with_type": 2,
                        "total_features": 0,
                        "total_tasks": 2,
                        "total_bugs": 0,
                        "total_features_done": 0,
                        "total_features_in_progress": 0,
                        "total": 4
                    },
                },
            }   
        }
        
        self.assertEqual(result, expected_result)

    def test_sense_iteracions_projects(self):

        data = {
            "project": {
            "1": {"title": "t1","assignee": None,"status": "Todo","item_type": "Issue","iteration":None,"issue_type": "Task"},
            "2": {"title": "t2","assignee": "member1","status": "In Progress","item_type": "Issue","iteration":None,"issue_type": "Task"},
            "3": {"title": "t3","assignee": "member1","status": "Todo","item_type": "DraftIssue","iteration":None},
            "4": {"title": "t4","assignee": "member2","status": "Done","item_type": "Issue","iteration":None,"issue_type": None},
            },
            "iterations": [
            ]
        }
        self.maxDiff = None
        result = self.collector.execute(data, self.metrics, self.members)
        expected_result = {
            "project": {
                "has_iterations" : False,
                "iterations": {
                },
                "metrics_by_iteration": {
                    "no_iteration": {
                        "assigned_per_member": {
                            "member1": 1,
                            "member2": 0,
                            "non_assigned": 1
                        },
                        "in_progress_per_member": {
                            "member1": 1,
                            "member2": 0
                        },
                        "done_per_member": {
                            "member1": 0,
                            "member2": 0
                        },
                        "in_progress": 1,
                        "done": 1,
                        "total_issues": 3,
                        "total_issues_with_type": 2,
                        "total_features": 0,
                        "total_tasks": 2,
                        "total_bugs": 0,
                        "total_features_done": 0,
                        "total_features_in_progress": 0,
                        "total": 4
                    },
                    "total": {
                        "assigned_per_member": {
                            "member1": 1,
                            "member2": 0,
                            "non_assigned": 1
                        },
                        "in_progress_per_member": {
                            "member1": 1,
                            "member2": 0
                        },
                        "done_per_member": {
                            "member1": 0,
                            "member2": 0
                        },
                        "in_progress": 1,
                        "done": 1,
                        "total_issues": 3,
                        "total_issues_with_type": 2,
                        "total_features": 0,
                        "total_tasks": 2,
                        "total_bugs": 0,
                        "total_features_done": 0,
                        "total_features_in_progress": 0,
                        "total": 4
                    }
                }
            },
        }
        
        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()