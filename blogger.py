#!/usr/bin/python
#
# Copyright (C) 2009 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# This file demonstrates how to use the Google Data API's Python client library
# to interface with the Blogger service.  There are examples for the following
# operations:
#
# * Retrieving the list of all the user's blogs
# * Retrieving all posts on a single blog
# * Performing a date-range query for posts on a blog
# * Creating draft posts and publishing posts
# * Updating posts
# * Retrieving comments
# * Creating comments
# * Deleting comments
# * Deleting posts

# Modified and updated by rickhau
# TODO
# Add command line to delete article

__author__ = 'lkeppler@google.com (Luke Keppler)'


import gdata.blogger.client
import gdata.client
import gdata.sample_util
import gdata.data
import atom.data
import argparse
import sys


class BloggerExample:

  def __init__(self):
    """Creates a GDataService and provides ClientLogin auth details to it.
    The email and password are required arguments for ClientLogin.  The
    'source' defined below is an arbitrary string, but should be used to
    reference your name or the name of your organization, the app name and
    version, with '-' between each of the three values."""

    # Authenticate using ClientLogin, AuthSub, or OAuth.
    self.client = gdata.blogger.client.BloggerClient()
    gdata.sample_util.authorize_client(
        self.client, service='blogger', source='Blogger_Python-2.0',
        scopes=['http://www.blogger.com/feeds/'])

    # Get the blog ID for the first blog.
    feed = self.client.get_blogs()
    self.blog_id = feed.entry[0].get_blog_id()

  def PrintUserBlogTitles(self):
    """Prints a list of all the user's blogs."""

    # Request the feed.
    feed = self.client.get_blogs()

    # Print the results.
    print feed.title.text
    for entry in feed.entry:
      print "\t" + entry.title.text
    print

  def CreatePost(self, title, content, is_draft):
    """This method creates a new post on a blog.  The new post can be stored as
    a draft or published based on the value of the is_draft parameter.  The
    method creates an GDataEntry for the new post using the title, content,
    author_name and is_draft parameters.  With is_draft, True saves the post as
    a draft, while False publishes the post.  Then it uses the given
    GDataService to insert the new post.  If the insertion is successful, the
    added post (GDataEntry) will be returned.
    """
    return self.client.add_post(self.blog_id, title, content, draft=is_draft)

  def PrintAllPosts(self):
    """This method displays the titles of all the posts in a blog.  First it
    requests the posts feed for the blogs and then it prints the results.
    """

    # Request the feed.
    feed = self.client.get_posts(self.blog_id)

    # Print the results.
    print feed.title.text
    for entry in feed.entry:
      if not entry.title.text:
        print "\tNo Title"
      else:
        print "\t" + entry.title.text
        # print "\t" + entry.title.text.encode('utf-8')
    print

  def PrintPostsInDateRange(self, start_time, end_time):
    """This method displays the title and modification time for any posts that
    have been created or updated in the period between the start_time and
    end_time parameters.  The method creates the query, submits it to the
    GDataService, and then displays the results.
  
    Note that while the start_time is inclusive, the end_time is exclusive, so
    specifying an end_time of '2007-07-01' will include those posts up until
    2007-6-30 11:59:59PM.

    The start_time specifies the beginning of the search period (inclusive),
    while end_time specifies the end of the search period (exclusive).
    """

    # Create query and submit a request.
    query = gdata.blogger.client.Query(updated_min=start_time,
                                       updated_max=end_time,
                                       order_by='updated')
    print query.updated_min
    print query.order_by
    feed = self.client.get_posts(self.blog_id, query=query)

    # Print the results.
    print feed.title.text + " posts between " + start_time + " and " + end_time
    print feed.title.text
    for entry in feed.entry:
      if not entry.title.text:
        print "\tNo Title"
      else:
        print "\t" + entry.title.text
    print

  def UpdatePostTitle(self, entry_to_update, new_title):
    """This method updates the title of the given post.  The GDataEntry object
    is updated with the new title, then a request is sent to the GDataService.
    If the insertion is successful, the updated post will be returned.

    Note that other characteristics of the post can also be modified by
    updating the values of the entry object before submitting the request.

    The entry_to_update is a GDatEntry containing the post to update.
    The new_title is the text to use for the post's new title.  Returns: a
    GDataEntry containing the newly-updated post.
    """
    
    # Set the new title in the Entry object
    entry_to_update.title = atom.data.Title(type='xhtml', text=new_title)
    return self.client.update(entry_to_update)

  def CreateComment(self, post_id, comment_text):
    """This method adds a comment to the specified post.  First the comment
    feed's URI is built using the given post ID.  Then a GDataEntry is created
    for the comment and submitted to the GDataService.  The post_id is the ID
    of the post on which to post comments.  The comment_text is the text of the
    comment to store.  Returns: an entry containing the newly-created comment

    NOTE: This functionality is not officially supported yet.
    """
    return self.client.add_comment(self.blog_id, post_id, comment_text)

  def PrintAllComments(self, post_id):
    """This method displays all the comments for the given post.  First the
    comment feed's URI is built using the given post ID.  Then the method
    requests the comments feed and displays the results.  Takes the post_id
    of the post on which to view comments. 
    """

    feed = self.client.get_post_comments(self.blog_id, post_id)

    # Display the results
    print feed.title.text
    for entry in feed.entry:
      print "\t" + entry.title.text
      print "\t" + entry.updated.text
    print

  def DeleteComment(self, comment_entry):
    """This method removes the comment specified by the given edit_link_href, the
    URI for editing the comment.
    """
    self.client.delete(comment_entry)

  def DeletePost(self, post_entry):
    """This method removes the post specified by the given edit_link_href, the
    URI for editing the post.
    """

    self.client.delete(post_entry)
  
  def run(self, newPostTitle, newPostFile):
    """Runs each of the example methods defined above, demonstrating how to
    interface with the Blogger service.
    """

    # Demonstrate retrieving a list of the user's blogs.
    #self.PrintUserBlogTitles()

    print "Current posts: "
    self.PrintAllPosts()    

    print '\t'+'-'*50
    feed = self.client.get_posts(self.blog_id)

    newPost = open(newPostFile)
    newPostHTMLContent = newPost.read()
    # Print the results.
    # print feed.title.text

    hasPosted = False
    for entry in feed.entry:
      #print entry.content.text # html
      if entry.content.text == newPostHTMLContent:
        print "\t\t== new Post was posted already!!! == "
        hasPosted = True
        break
    print

    if not hasPosted:
        print "Posting new post: ", newPostTitle
        self.CreatePost(title=newPostTitle, content=newPostHTMLContent, is_draft=False)
    
    print '\t'+'-'*50
    print "After new post: "
    self.PrintAllPosts()

class HelpAction(argparse.Action):

    def __call__(self, parser, namespace, values, option_string=None):
        parser.print_help()
        print("""

To publish html file to blogger as a new post with title:

  $ blogger --title="This is a new title" --file 2015-3-17.html

OR

  $ blogger -t="NEW TITLE" -f 2015-3-20.html

  Then, choose 1) to use your gmail account to post the new article(html)
""")
        sys.exit(0)

def main():
  """The main function runs the BloggerExample application.
  
  NOTE:  It is recommended that you run this sample using a test account.
  """
  parser = argparse.ArgumentParser(
    description='Post your HTML article to Blogger.',
    add_help=False,
  )
  parser.add_argument(
    '--help', '-h',
    action=HelpAction,
    nargs=0,
    help='show this help message and exit',
  )
  parser.add_argument(
    '--title', '-t',
    help='Title for this new post',
    default='Test Article',
    action='store',
    dest='title',
  )
  parser.add_argument(
    '--file', '-f',
    help='HTML file to process(converted from .md to .html)',
    action='store',
    dest='filename'
  )    
  args = parser.parse_args()

  print "title: ", args.title
  print "filename: ", args.filename

  if not args.filename:
    print "Please input the html file for posting..."
    print "$ blogger --title='This is a new title' --file 2015-3-17.html"
    exit(1)
    
  sample = BloggerExample()
  sample.run(newPostTitle=args.title, newPostFile=args.filename)


if __name__ == '__main__':
  main()
