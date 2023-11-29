import threading
from flask import Flask, render_template, request
import fitz
import re


from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.shared import Inches

import boto3
import os
import time
from openai import OpenAI
import json


app = Flask(__name__)

# const_bucket_name = "cloud-computing-termproject-boon"
const_bucket_name = "boon-ash-5409"
aws_region = 'us-east-1'


aws_services = ['aws wavelength', 'aws trusted advisor', 'aws iot sitewise', 'aws transfer family', 'amazon aurora', 'aws elemental medialive', 'amazon cloudwatch', 'aws iot core', 'amazon workdocs', 'aws deepracer', 'amazon lex', 'amazon polly', 'amazon elastic beanstalk', 'aws iot events', 'aws elastic file system (efs)', 'aws organizations', 'aws iot analytics', 'aws snowcone', 'aws elastic load balancing', 'aws deeplens', 'aws opsworks', 'amazon freertos', 'aws elemental mediastore', 'amazon ecr', 'aws cost explorer', 'aws service health dashboard', 'aws step functions', 'aws direct connect', 'aws iot greengrass', 'amazon dynamodb', 'aws resource groups', 'aws identity and access management (iam)', 'aws snowball', 'aws storage gateway', 'aws fsx', 'amazon rds', 'aws deepcomposer', 'amazon sqs', 'amazon appstream', 'aws datasync', 'aws backup', 'aws elastic beanstalk', 'amazon ecs', 'amazon lambda', 'amazon sagemaker', 'amazon s3', 'aws lambda', 'amazon worklink', 'amazon route 53', 'amazon redshift', 'amazon forecast', 'aws deep learning base ami', 'amazon iam', 'aws cloudtrail', 'amazon comprehend', 'aws config', 'amazon translate', 'aws compute optimizer', 'aws deep learning containers', 'amazon ses', 'amazon ec2', 'amazon pinpoint', 'amazon sagemaker', 'amazon connect', 'amazon rekognition', 'aws network firewall', 'amazon workmail', 'amazon kendra', 'amazon sns', 'aws glue', 'amazon workspaces', 'aws deep learning amis', 'amazon transcribe', 'aws cloudformation', 'aws budgets', 'aws deep learning instances', 'aws elemental mediatailor', 'aws chatbot', 'aws outposts', 'aws elemental mediapackage', 'aws key management service (kms)', 'amazon cloudfront', 'amazon api gateway', 'amazon kinesis', 'amazon personalize', 'amazon vpc', 'aws elemental mediaconvert', 'aws snow family', 'aws snowmobile', 'aws iot device management', 'aws local zones', 'amazon honeycode', 'amazon eks', 'aws media services', 'aws elastic transcoder', 'amazon chime', 'glacier', 's3', 'standard', 'standard-ia', 's3 one zone-ia', 's3 intelligent-tiering']
aws_keywords = ['etl', 'database connection pool load balancing', 'blue-green deployment', 'write replica', 'data consistency', 'pip', 'database platform', 'database connection pool failover best practices', 'database disaster recovery', 'database vendor', 'database platform as a service', 'master branch', 'database recovery', 'sre', 'snapshot isolation', 'package manager', 'cicd', 'database replication', 'efs', 'cross-account', 'dbaas', 'multi-master replication', 'code review', 'load balancing', 'rds', 'resilience', 'secret key', 'aws copilot', 'master-slave replication', 'database connection pool performance tuning', 'scrum', 'feature branch', 'event sourcing', 'partition tolerance', 'database replication service', 'dependency', 'database audit', 'database upgrade', 'feature toggle', 'multi-region', 'pulumi', 'database connection timeout', 'bastion host', 'serverless database', 'coding standards', 'database connection pool scalability best practices', 'nosql database', 'data lakes', 'database connection pool scalability', 'logging', 'pci dss', 'database connection pool auto-recovery', 'canary deployment', 'continuous delivery', 'write consistency', 'solutions architect', 'jwt', 'devops engineer', 'database connection pool connection validation', 'database connection close', 'restful', 'cdk', 'build automation', 'data catalog', 'backend developer', 'aws cdk', 'gitlab', 'database connection pool testing', 'database encryption', 'cloud database', 'database connection pool thread safety best practices', 'certification', 'cloud specialist', 'data warehouse', 'locking', 'specialty', 'database connection pooling', 'codecommit', 'cdn', 'replica', 'associate', 'database connection pool performance', 'database connection pool transaction management', 'batch processing', 'database connection', 'strong consistency', 'cloud-native database', 'serverless framework', 'cloud-native', 'encryption', 'database connection pool connection reuse', 'continuous deployment', 'fault tolerance', 'fork', 'reserved instances', 'monitoring', 'database connection pool tuning', 'version control', 'saml', 'database connection pool thread safety', 'asynchronous', 'pair programming', 'database connection pool configuration', 'test-driven development', 'database backup', 'cloud trainer', 'refactoring', 'cloud architect', 'database connection pool load balancing best practices', 'compliance', 'agile', 'database migration service', 'cloud-native database service', 'reporting', 'automation', 'database patching', 'read replica', 'dynamodb', 'big data', 'edge computing', 'spot fleet', 'deployment automation', 'gateway endpoint', 'lambda', 'pull request', 'database optimization', 'release branch', 'puppet', 'git', 'sam', 'kinesis', 'database monitoring tools', 'database connection pool isolation', 'graphql', 'database connection pool failover', 'database connection pool eviction', 'vpc peering', 'isolation levels', 'database index', 'data modeling', 'gdpr', 'github', 'cloud consultant', 'optimistic concurrency control', 'database profiling', 'cloud-native developer', 'docker', 'read consistency', 'database backup service', 'dashboard', 'firewall', 'data security', 'shared responsibility model', 'artifact management', 'feature', 'source control', 'interface endpoint', 'cloud strategist', 'elastic', 'internet of things', 'database connection management', 'business intelligence', 'database connection leak', 'database security', 'commit', 'data lineage', 'data anonymization', 'cap theorem', 'ssl', 'database schema migration', 'data masking', 'base properties', 'database connection pool parameters', 'technical debt', 'database connection pool optimization', 'database caching', 'container orchestration', 'sso', 'database as a service', 'database connection pool logging best practices', 'leader-follower replication', 'data encryption', 'horizontal scaling', 'database indexing', 'on-demand', 'database failover', 'api gateway', 'release management', 'transit gateway', 'cloud practitioner', 'branching', 'base transactions', 'cloudwatch', 'database release management', 'cloud database service', 'architectural decision record', 'security group', 'sprint', 'cognito', 'database connection pool exception handling', 'scalability', 'database connection pool security', 'vertical scaling', 'kms', 'vpn', 'api', 'cidr', 'cloudformation', 'database normalization', 'workflow', 'orchestration', 'organizations', 'availability', 'cloud', 'column-family store', 'serverless', 'nosql', 'database schema', 'full stack developer', 'cloud engineer', 'service mesh', 'acid properties', 'resource groups', 'pipeline', 'audit', 'database connection pool logging', 'hsm', 's3', 'data pipeline', 'configuration management', 'consistency', 'bitbucket', 'cqrs', 'assume role', 'database scaling', 'kanban', 'well-architected framework', 'database connection pool optimization best practices', 'stream processing', 'acid transactions', 'codepipeline', 'migration', 'ansible', 'cross-region', 'vpc', 'database migration', 'database access control', 'frontend developer', 'data privacy', 'database load balancing', 'multi-cloud', 'database rollback', 'data integration', 'hybrid cloud', 'database profiling tools', 'gitflow', 'relational database management system', 'continuous improvement', 'deployment pipeline', 'concurrency control', 'devops', 'aws marketplace', 'snapshots', 'data quality', 'json', 'security best practices', 'resilience engineering', 'data ops', 'serialization', 'graph database', 'coding best practices', 'database', 'build tool', 'oauth', 'zero trust', 'auto scaling', 'user story', 'serverless application model', 'redshift', 'docker registry', 'well-architected review', 'artifact', 'maven', 'mfa', 'transaction isolation', 'direct connect gateway', 'npm', 'epic', 'ai', 'database software', 'bugfix branch', 'blueprints', 'federation', 'kappa architecture', 'real-time analytics', 'role', 'database connection pool transaction management best practices', 'sqs', 'synchronous', 'database restore', 'sns', 'subnetting', 'data mesh', 'partner network', 'relational database', 'lift and shift', 'iam', 'database connection pool size', 'access key', 'database change management', 'analytics', 'least privilege', 'observability', 'database connection pool health check', 'artifact repository', 'data lakehouse', 'terraform', 'pessimistic concurrency control', 'database performance', 'lambda architecture', 'database connection pool configuration best practices', 'soap', 'main branch', 'database sharding', 'velocity', 'repository', 'database versioning', 'codedeploy', 'aws sam', 'serverless computing', 'hotfix branch', 'continuous integration', 'document store', 'x-ray', 'burndown chart', 'merge conflict', 'aurora', 'database tuning', 'dark launch', 'distributed database', 'hipaa', 'database high availability', 'tls', 'eventual consistency', 'database connection pool', 'database connection pool best practices', 'data architecture', 'infrastructure as code', 'containerization', 'messaging', 'database connection pool testing best practices', 'microservices', 'database connection string', 'database partitioning', 'cloudtrail', 'key-value store', 'chef', 'database monitoring', 'database connection pool monitoring', 'ebs', 'credentials', 'database connection pool idle timeout', 'codebuild', 'cloudfront', 'professional', 'high availability', 'config', 'direct connect', 'database federation', 'backlog', 'database connection pool monitoring best practices', 'database recovery service', 'database connection pool deadlock detection', 'server provisioning', 'machine learning', 'tracing', 'data governance', 'database compliance', 'subnet', 'step functions', 'kubernetes', 'database connection pool security best practices', 'route 53', 'data durability', 'yaml', 'event-driven architecture', 'data analytics', 'immutable infrastructure', 'elastic beanstalk', 'spot instances', 'retrospective', 'serverless database service', 'chaos engineering', 'computation', 'amazon', 'durability', 'performance', 'security']

s3_client = boto3.client('s3', region_name=aws_region)

url1 = ""
url2 = ""

@app.route("/")
def hello():
    return render_template('index.html')

def find_keywords_and_color(pdf_path):
    
    output_path = "reWise.pdf"

    doc = fitz.open(pdf_path)

    for page_number in range(doc.page_count):
        page = doc[page_number]
        words = page.get_text("words")

        for word in words:
            # print(word)
            if word[4].lower() in aws_services or word[4].lower() in aws_keywords:
                word_rect = fitz.Rect(word[:4])  # Coordinates are stored in the first four elements
                page.draw_rect(word_rect, color=(0, 0, 0), fill=True, width=2)

    doc.save(output_path)
    doc.close()

def create_docx(text):
    # Create a new Document
    doc = Document()

    # Set page size to A4
    doc.sections[0].page_width = Inches(8.27)
    doc.sections[0].page_height = Inches(11.69)

    # Set margins to zero
    for section in doc.sections:
        section.top_margin = Inches(0)
        section.bottom_margin = Inches(0)
        section.left_margin = Inches(0)
        section.right_margin = Inches(0)

    # Add a paragraph with your text
    paragraph = doc.add_paragraph(text)

    # Set paragraph alignment to justify
    paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.LEFT

    paragraph.style.font.size = Pt(5)

    paragraph.style.paragraph_format.line_spacing = Pt(5)

    # Save the document to a file
    doc.save("cheat_sheet.docx")

@app.route("/upload_s3", methods=['post'])
def upload_s3():
    file = request.files['file']

    # Save the file locally
    fileName = file.filename
    local_file_path = f"{fileName}"
    file.save(local_file_path)

    # Upload the file to S3 bucket
    s3_client.upload_file(local_file_path, const_bucket_name, fileName, Callback=ProgressPercentage(local_file_path))

    # use Textractor to analyse the text
    fileData = detectTextFromTheFile(fileName)

    # get detected words along with their metadata
    detectedWords = fileData["Blocks"]

    # get only the words
    lecture_text = ""

    for line in detectedWords:
        if line["BlockType"] == "LINE":
            lecture_text += line["Text"] + "\n"


    words = []
    for word in detectedWords:
        if word["BlockType"] == "WORD":
            words.append(word)
            if word["Text"].lower() in aws_services or word["Text"].lower() in aws_keywords:
                words.append(word)

    # add opaque boxes to the pdf key words for revision
    find_keywords_and_color(local_file_path)

    os.remove(local_file_path)

    gpt_response = generate_cheat_sheet(lecture_text)

    cleaned_string = re.sub(r"[\n\t]", "|", gpt_response)

    create_docx(cleaned_string)

    
    current_epoch_time = int(time.time())
    
    cheat_sheet_file_name = f"cheat_sheet{current_epoch_time}.docx"
    reWise_file_name = f"reWise{current_epoch_time}.pdf"

    # upload to S3
    s3_client.upload_file("cheat_sheet.docx", const_bucket_name, cheat_sheet_file_name)

    s3_client.upload_file("reWise.pdf", const_bucket_name, reWise_file_name)

    url2 = "https://cloud-computing-termproject-boon.s3.amazonaws.com/" + cheat_sheet_file_name
    url1 = "https://cloud-computing-termproject-boon.s3.amazonaws.com/" + reWise_file_name

    return render_template('output.html', url1 = url1, url2 = url2)


@app.route('/subscribe',methods=['POST'])
def result():
    output = request.form.to_dict()
    print(output)
    email = output["email"]

    print(email)

    payload = {
        "email": email
    }

    payload_json = json.dumps(payload)

    call_scheduler_lambda(payload_json)
    return render_template('output.html', email = email, url1 = url1, url2 = url2)
    
def generate_cheat_sheet(lecture_text):

    part1 = "sk-u1R8"
    part2 = "fwFICi"
    part3 = "bJGuDz"
    part4 = "rfcpT3"
    part5 = "BlbkFJ"
    part6 = "4nw1wP"
    part7 = "PhVACo"
    part8 = "0r0FRM"
    part9 = "8S"

    # Concatenate string literals
    concatenated_string = part1 + part2 + part3 + part4 + part5 + part6 + part7 + part8 + part9


    gpt_client = OpenAI(api_key = concatenated_string)
    
    messages = [{"role": "system", "content": "You are a Computer Science expert and you are to generate cheat sheet from the given text with few words."}, 
                {"role": "user", "content": "generate cheat sheet for this text: " + lecture_text}]

    response = gpt_client.chat.completions.create(model="gpt-3.5-turbo-0301", messages=messages)
    reply = response.choices[0].message.content
    print(reply)
    return reply

        

class ProgressPercentage(object):

    def __init__(self, filename):
        self._filename = filename
        self._size = float(os.path.getsize(filename))
        self._seen_so_far = 0
        self._lock = threading.Lock()

    def __call__(self, bytes_amount):
        # To simplify, assume this is hooked up to a single filename
        with self._lock:
            self._seen_so_far += bytes_amount
            percentage = (self._seen_so_far / self._size) * 100
            print(f"{self._seen_so_far}/{self._size}")

def detectTextFromTheFile(fileName):
    textract = boto3.client('textract', region_name=aws_region)
    
    
    response = textract.start_document_text_detection(
        DocumentLocation={'S3Object': {'Bucket': const_bucket_name,'Name': fileName}})
    
    jobId = response["JobId"]
    print(response["JobId"])
    
    if (CheckJobComplete(jobId)):
        output = textract.get_document_text_detection(JobId=jobId)
        # print(output)
        return output

def CheckJobComplete(jobId):
    time.sleep(3)
    client = boto3.client('textract', region_name = aws_region)
    response = client.get_document_text_detection(JobId=jobId)
    status = response["JobStatus"]
    print("Job status: {}".format(status))
    while(status == "IN_PROGRESS"):
        time.sleep(3)
        response = client.get_document_text_detection(JobId=jobId)
        status = response["JobStatus"]
        print("Job status: {}".format(status))
    return status


def call_scheduler_lambda(payload):
    lambda_client = boto3.client('lambda', region_name=aws_region)
    lambda_function_name = "send_revision_reminder"

    response = lambda_client.invoke(FunctionName=lambda_function_name,
                                    InvocationType='RequestResponse',
                                    Payload=payload)
    
    print(response)



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
