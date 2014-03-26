from xml.dom import minidom
import urllib2

class Course:

	def __init__(self, year, subject, code, title, description):

		self.year = year
		self.subject = subject
		self.code = code
		self.title = title
		self.description = description
		self.rank = 0

	@property
	def fullCode(self):
		return self.subject + self.code

class ExploreCourses:

	def __init__(self):

		self.base_url = 'http://explorecourses.stanford.edu/CourseSearch/search?view=xml-20130201&catalog=&page=0&filter-coursestatus-Active=on'

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

		# Return the object array
		return courses

	# Retrieves the best match for a course
	def getCourse(self, course):

		# First get the list of courses that match
		results = self.query(course)

		# Cache the best result here
		bestScore = 0
		bestResult = None

		# Iterate through the results and find the best one
		for result in results:

			# Get the LCS between the query and the course title
			score = self.longestCommonSubstring(course, result.fullCode)

			# We use this as the similarity metric
			if score > bestScore:

				# Set these results as the new "best results"
				bestScore = score
				bestResult = result

		# Return the best result
		return bestResult

	# Get the text from a tag element
	def getText(self, course, element):

		return course.getElementsByTagName(element)[0].firstChild.nodeValue

	# Calculates the longest common substring between two strings
	def longestCommonSubstring(self, str1, str2):

		# Get the lengths of both of our strings
		len1 = len(str1)
		len2 = len(str2)

		# Array caches the distances
		arr = [[0 for i in range(len2+1)] for j in range(len1+1)]

		for i in range(0, len1+1):
			arr[i][0] = 0

		for j in range(0, len2+1):
			arr[0][j] = 0

		for i in range(0, len1):
			for j in range(0, len2):
				if str1[i] == str2[j]:
					arr[i][j] = arr[i-1][j-1] + 1
				else:
					if i > 0 and j > 0:
						arr[i][j] = max(arr[i][j-1], arr[i-1][j])
					elif i == 0 and j > 0:
						arr[i][j] = arr[0][j-1]
					elif i > 0 and j == 0:
						arr[i][j] = arr[i-1][j]

		return arr[len1-1][len2-1]
