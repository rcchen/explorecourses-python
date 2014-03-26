from xml.dom import minidom
import urllib2

class Schedule:

	def __init__(self, startDate, endDate, startTime, endTime, location, days):

		self.startDate = startDate
		self.endDate = endDate
		self.startTime = startTime
		self.endTime = endTime
		self.location = location
		self.days = days

class Section:

	def __init__(self, classId, term, subject, code, units, sectionNumber, component, courseId):

		self.classId = classId
		self.term = term
		self.subject = subject
		self.code = code
		self.units = units
		self.sectionNumber = sectionNumber
		self.component = component
		self.courseId = courseId
		self.schedules = []

class Course:

	def __init__(self, year, subject, code, title, description, gers, repeatable, grading, unitsMin, unitsMax):

		self.year = year
		self.subject = subject
		self.code = code
		self.title = title
		self.description = description
		self.gers = gers
		self.repeatable = repeatable
		self.grading = grading
		self.unitsMin = unitsMin
		self.unitsMax = unitsMax
		self.sections = []

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
			gers = self.getText(dom_course, 'gers')
			courseId = self.getText(dom_course, 'courseId')
			repeatable = self.getText(dom_course, 'repeatable')
			grading = self.getText(dom_course, 'grading')
			unitsMin = self.getText(dom_course, 'unitsMin')
			unitsMax = self.getText(dom_course, 'unitsMax')

			# Create a new Course
			course = Course(year, subject, code, title, description, gers, repeatable, grading, unitsMin, unitsMax)

			# Get the sections
			dom_sections = dom_course.getElementsByTagName('section')

			# Create section objects
			for dom_section in dom_sections:

				# Create the section
				section = self.handleSection(dom_section)

				# Add it to our array
				course.sections.append(section)

			# Save it into our array
			courses.append(course)

		# Return the object array
		return courses

	def handleSection(self, dom_section):

		# Extract data from the DOM
		classId = self.getText(dom_section, 'classId')
		term = self.getText(dom_section, 'term')
		subject = self.getText(dom_section, 'subject')
		code = self.getText(dom_section, 'code')
		units = self.getText(dom_section, 'units')
		sectionNumber = self.getText(dom_section, 'sectionNumber')
		component = self.getText(dom_section, 'component')
		courseId = self.getText(dom_section, 'courseId')

		# Create a new section
		section = Section(classId, term, subject, code, units, sectionNumber, component, courseId)

		# Get the schedules
		dom_schedules = dom_section.getElementsByTagName('schedule')

		# Create schedule objects
		for dom_schedule in dom_schedules:

			# Create the schedule
			schedule = self.handleSchedule(dom_schedule)

			# Add it to our array
			section.schedules.append(schedule)

		# Return our new instance
		return section

	def handleSchedule(self, dom_schedule):

		# Extract data from the DOM
		startDate = self.getText(dom_schedule, 'startDate')
		endDate = self.getText(dom_schedule, 'endDate')
		startTime = self.getText(dom_schedule, 'startTime')
		endTime = self.getText(dom_schedule, 'endTime')
		location = self.getText(dom_schedule, 'location')
		days = self.getText(dom_schedule, 'days')

		# Create a new schedule
		schedule = Schedule(startDate, endDate, startTime, endTime, location, days)

		# Return our new instance
		return schedule

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
	def getText(self, dom_object, element):

		# Attempt to fetch the text target
		target = dom_object.getElementsByTagName(element)[0].firstChild

		# Check to see if the target exists
		if target is not None:
			return target.nodeValue
		else:
			return ""		

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
