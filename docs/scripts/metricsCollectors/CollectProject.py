from .CollectorBase import CollectorBase
from datetime import datetime, timedelta

class CollectProject(CollectorBase):
    def execute(self, data: dict, metrics: dict, members) -> dict:
        draftIssues = data['project']
        iterations_data = data['iterations']
        iterations = {}
        assigned_draftIssue_per_member = {member: 0 for member in members}
        done_assigned_draftIssues_per_member = {member: 0 for member in members}
        in_progress_assigned_draftIssues_per_member = {member: 0 for member in members}
        non_assigned = 0
        total = 0
        total_done = 0
        total_in_progress = 0
        total_issues = 0
        total_issues_with_type = 0
        total_features = 0
        total_tasks = 0
        total_bugs = 0
        for _,draftIssue in draftIssues.items():
            total +=1
            if draftIssue['status'] == 'Done':
                total_done += 1
            elif draftIssue['status'] == 'In Progress':
                total_in_progress += 1
            if draftIssue['item_type'] == 'Issue':
                total_issues +=1
                if draftIssue['issue_type'] != None:
                    total_issues_with_type +=1
                    if draftIssue['issue_type'] == "Feature":
                        total_features += 1
                    elif draftIssue['issue_type'] == "Bug":
                        total_bugs +=1
                    elif draftIssue['issue_type'] == "Task":
                        total_tasks += 1
                        if draftIssue['assignee'] != None and draftIssue['assignee'] in members:
                            assigned_draftIssue_per_member[draftIssue['assignee']] +=1
                            if draftIssue['status'] == 'Done':
                                done_assigned_draftIssues_per_member[draftIssue['assignee']] += 1
                            elif draftIssue['status'] == 'In Progress':
                                in_progress_assigned_draftIssues_per_member[draftIssue['assignee']] +=1
                        else:
                            non_assigned += 1

        has_iterations = False
        for iteration in iterations_data:
            has_iterations = True
            start_date_str = iteration['startDate']
            duration_days = iteration['duration'] 
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
            end_date = start_date + timedelta(days=duration_days)
            end_date_str = end_date.strftime("%Y-%m-%d")
            iterations[iteration['id']] = {
                "title" : iteration['title'],
                "startDate" : start_date_str,
                "endDate" : end_date_str,
                "duration" :duration_days
            }
        assigned_draftIssue_per_member['non_assigned'] = non_assigned
        metrics['project']= {
            'assigned_per_member': assigned_draftIssue_per_member,
            'in_progress_per_member': in_progress_assigned_draftIssues_per_member,
            'done_per_member': done_assigned_draftIssues_per_member,
            'has_iterations': has_iterations,
            'iterations' : iterations,
            'in_progress': total_in_progress,
            'done': total_done,
            "total_issues": total_issues,
            "total_issues_with_type": total_issues_with_type,
            "total_features":total_features,
            "total_tasks": total_tasks,
            "total_bugs" : total_bugs,
            'total': total
        }
        return metrics
         
