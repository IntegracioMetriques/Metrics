from .CollectorBase import CollectorBase

class CollectIssues(CollectorBase):
    def execute(self, data: dict, metrics: dict, members) -> dict:
        issues = data['issues']
        assigned_issues_per_member = {member: 0 for member in members}
        closed_assigned_issues_per_member = {member: 0 for member in members}
        non_assigned = 0
        total = 0
        for _,issue in issues.items():
            if issue['assignee'] != None and issue['assignee'] in members:
                assigned_issues_per_member[issue['assignee']] +=1
                if issue['state'] == 'closed':
                    closed_assigned_issues_per_member[issue['assignee']] += 1
            else:
                non_assigned += 1
            total += 1
        metrics['issues']= {'assigned': assigned_issues_per_member
        }
        metrics['issues']['assigned']['non_assigned'] = non_assigned
        metrics['issues']['closed'] = closed_assigned_issues_per_member
        metrics['issues']['total'] = total
        return metrics
         