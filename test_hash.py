# Python program to find the SHA-1 message digest of a file

# importing the hashlib module
import hashlib

def hash_file(filename):
   """"This function returns the SHA-1 hash
   of the file passed into it"""

   # make a hash object
   h = hashlib.sha1()

   # open file for reading in binary mode
   with open(filename,'rb') as file:

       # loop till the end of the file
       chunk = 0
       while chunk != b'':
           # read only 1024 bytes at a time
           chunk = file.read(1024)
           h.update(chunk)

   # return the hex representation of digest
   return h.hexdigest()

a = hash_file("sces/2005.11401v4.pdf")
# a = hash_file("sces/2023 Q3 NVDA.pdf")
print(a)
print(len(a))


# import boto3
# import botocore

# # def s3_md5sum(bucket_name, resource_name):
# #     try:
# #         md5sum = boto3.client('s3').head_object(
# #             Bucket=bucket_name,
# #             Key=resource_name
# #         )['ETag'][1:-1]
# #     except botocore.exceptions.ClientError:
# #         md5sum = None
# #         pass
# #     return md5sum
