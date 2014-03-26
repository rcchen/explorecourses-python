from xml.dom import minidom
import urllib2

class Course:

	def __init__(self, year, subject, code, title, description):

		self.year = year
		self.subject = subject
		self.code = code
		self.title = title
		self.description = description

class ExploreCourses:

	def __init__(self):

		self.base_url = 'http://explorecourses.stanford.edu/CourseSearch/search?view=xml-20130201&catalog=&page=0&filter-coursestatus-Active=on'
		self.courses = []

	def query(self, query):

		# Assemble the query string
		url = self.base_url + '&q=' + query

		# Retrieve the XML from the URL
		data = urllib2.urlopen(url)

		# Parse using Minidom
		dom = minidom.parse(data)

		# Retrieve all of the courses
		dom_courses = dom.getElementsByTagName('course')

		# Get the classes
		courses = []

		# Now parse each one into a course object
		for dom_course in dom_courses:

			# Retrieve things from 
			year = self.getText(dom_course, 'year')
			subject = self.getText(dom_course, 'subject')
			code = self.getText(dom_course, 'code')
			title = self.getText(dom_course, 'title')
			description = self.getText(dom_course, 'description')

			# Create a new Course
			course = Course(year, subject, code, title, description)

			# Save it into our array
			courses.append(course)

		return courses

	def getText(self, course, element):

		return course.getElementsByTagName(element)[0].firstChild.nodeValue



