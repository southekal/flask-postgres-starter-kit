import boto3


def process_text_detection(bucket, document):
	"""
		reference: https://docs.aws.amazon.com/code-samples/latest/catalog/python-textract-textract_python_detect_document_text.py.html
		- looks up s3 document
		- extracts text per LINE
	"""

	#Get the document from S3
	s3_connection = boto3.resource('s3')
	                  
	s3_object = s3_connection.Object(bucket, document)
	s3_response = s3_object.get()

	# Detect text in the document
	client = boto3.client('textract')
	
	#process using S3 object
	response = client.detect_document_text(
		Document={'S3Object': {'Bucket': bucket, 'Name': document}}
	)

	#Get the text blocks
	blocks = response['Blocks']
	
	line_holder = []
	for block in blocks:
		if block['BlockType'] == 'LINE':
			line_holder.append(block["Text"])

	return line_holder
