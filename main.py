from bs4 import BeautifulSoup
import requests

class Job:

    def __init__(self, name, description, location, salary, recruiter, days_since_posting, days_left):

        self.name = name
        self.description = description
        self.location = location
        self.salary = salary
        self.recruiter = recruiter
        self.days_since_posting = days_since_posting
        self.days_left = days_left

    def __str__(self):
        return (
            f'Job name: {self.name}\n'
            f'Job description: {self.description}\n'
            f'Location: {self.location}\n'
            f'Salary: {self.salary}\n'
            f'Recruiter: {self.recruiter}\n'
            f'Days since posting: {self.days_since_posting if self.days_since_posting is not None else 'unknown'}\n'
            f'Days left: {self.days_left if self.days_left is not None else 'unknown'}'
        )
    
    def check_if_timely(self):
        return self.days_since_posting and self.days_since_posting <= 3 or self.days_left and self.days_left <= 10
    
class Director_Job(Job):

    def __init__(self, name, description, location, salary, recruiter, days_since_posting, days_left):
        super.__init__(self, name, description, location, salary, recruiter, days_since_posting, days_left)

    def make_esteemed_job_description(self):

        return f'You will be a DIRECTOR in {self.location}!'

class Job_List_Fetcher:
    
    @staticmethod
    def __get_page_soup():

        html_text = requests.get('https://appointments.thetimes.co.uk/jobs/').content
        return BeautifulSoup(html_text, 'lxml')

    @staticmethod
    def __make_populated_job(job_node):

        date_node = job_node.find(class_='pipe')
        deadline_node = date_node.find(class_='text-error')

        return Job(
            name=job_node.find(class_='lister__header').a.span.text,
            description=job_node.find(class_='lister__description').text,
            location=job_node.find(class_='lister__meta-item--location').text,
            salary=job_node.find(class_='lister__meta-item--salary').text,
            recruiter=job_node.find(class_='lister__meta-item--recruiter').text,
            days_since_posting=None if deadline_node else int(date_node.text.split()[0]),
            days_left=int(deadline_node.text.split()[0]) if deadline_node else None
        )

    @staticmethod
    def __get_job_node_list(soup):

        return soup.find_all(class_='lister__item')

    @staticmethod
    def __get_job_list(soup):

        job_node_list = Job_List_Fetcher.__get_job_node_list(soup)
        job_list = [Job_List_Fetcher.__make_populated_job(job_node) for job_node in job_node_list]
        return job_list

    @staticmethod
    def get_the_times_job_list():

        page_soup = Job_List_Fetcher.__get_page_soup()
        return Job_List_Fetcher.__get_job_list(page_soup)

if __name__ == '__main__':

    job_list = Job_List_Fetcher.get_the_times_job_list()
    timely_jobs = [job for job in job_list if job.check_if_timely()]
    for job in timely_jobs:
        print(job)
        print('---')
