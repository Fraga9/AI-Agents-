from crewai import Task


class AISoftwareCompanyTasks():
    def set_high_level_requirements_task(self, agent):
        return Task(
            description="Define the overall vision, goals, and strategic direction of the project."
            agent=agent,
            asynch_execution=True,
            expected_output="""A list of directives and tasks to do.
                        Example output:
                        'Project Vision: Create an innovative web application that improves user engagement through real-time collaboration features.
                        Strategic Goals: 
                        1. Increase user retention by 25% within the first year.
                        2. Achieve a 4.5-star rating in app stores.
                        3. Integrate advanced security features to ensure data privacy.'      
            """
        )
    
    def write_PRD_task(self, agent, context):
        return Task(
            description="Develop detailed documents that outline the product's objectives, scope, features, user stories, and acceptance criteria."
            agent=agent,
            asynch_execution=True,
            context=context,
            expected_output="""A list of bullet points to describe respectively : 'Product name', 'Objectives', 'Features', 'User stories', 'Acceptance criteria'.
                        Example output:
                        'Product Name: Real-Time Collaboration Web App
                        Objectives: 
                        - Enable real-time document editing and collaboration.
                        - Provide seamless user experience across different devices.
                        Features:
                        - User Authentication and Profile Management.
                        - Real-time Document Editing with Version Control.
                        User Stories:
                        - As a user, I want to create and edit documents in real-time with my team.
                        - As a user, I want to receive notifications when someone comments on my document.
                        Acceptance Criteria:
                        - The application should allow multiple users to edit the same document simultaneously.
                        - Changes should be visible to all users in real-time without page refresh.'
            """
        )
    
    def revise_PRD_task(self, agent, context):
        return Task(
            description="Continuously update and refine the PRD based on feedback and changing requirements."
            agent=agent,
            asynch_execution=True,
            context=context,
            expected_output="""A list of bullet points to describe respectively : 'Product name', 'Objectives', 'Features', 'User stories', 'Acceptance criteria'.
                        Example output:
                        'Product Name: Real-Time Collaboration Web App
                        Objectives: 
                        - Enable real-time document editing and collaboration.
                        - Provide seamless user experience across different devices.
                        Features:
                        - User Authentication and Profile Management.
                        - Real-time Document Editing with Version Control.
                        User Stories:
                        - As a user, I want to create and edit documents in real-time with my team.
                        - As a user, I want to receive notifications when someone comments on my document.
                        Acceptance Criteria:
                        - The application should allow multiple users to edit the same document simultaneously.
                        - Changes should be visible to all users in real-time without page refresh.'
            """
        )
     
    def write_design_task(self, agent, context):
        return Task(
            description="Create comprehensive design documents detailing the system architecture, design patterns, data flow, and technical specifications.",
            agent=agent,
            asynch_execution=True,
            context=context,
            expected_output="""A structured document including sections on system architecture, design patterns, data flow, and technical specifications.
                        Example output:
                        'System Architecture:
                        - Frontend: React.js with Redux for state management.
                        - Backend: Node.js with Express.js for API development.
                        - Database: MongoDB for scalable data storage.
                        - Real-Time Communication: WebSocket for real-time updates.
                        Design Patterns:
                        - MVC (Model-View-Controller) for backend structure.
                        - Singleton pattern for managing WebSocket connections.
                        Data Flow:
                        - User actions are captured by the frontend and sent to the backend via RESTful APIs.
                        - Backend processes the data and updates the MongoDB database.
                        - Real-time updates are pushed to clients using WebSocket.
                        Technical Specifications:
                        - The frontend should support all modern browsers and devices.
                        - The backend must handle up to 10,000 concurrent users.'"""
        )
    
    def revise_design_task(self, agent, context):
        return Task(
            description="Continuously update and refine the PRD based on feedback and changing requirements.",
            agent=agent,
            asynch_execution=True,
            context=context,
            expected_output="""A list of bullet points to describe respectively : 'Product name', 'Objectives', 'Features', 'User stories', 'Acceptance criteria'.
                        Example output:
                        'Product Name: Real-Time Collaboration Web App
                        Objectives: 
                        - Enable real-time document editing and collaboration.
                        - Provide seamless user experience across different devices.
                        Features:
                        - User Authentication and Profile Management.
                        - Real-time Document Editing with Version Control.
                        User Stories:
                        - As a user, I want to create and edit documents in real-time with my team.
                        - As a user, I want to receive notifications when someone comments on my document.
                        Acceptance Criteria:
                        - The application should allow multiple users to edit the same document simultaneously.
                        - Changes should be visible to all users in real-time without page refresh.'
            """
        )
    
    def review_PRD_task(self, agent, context):
        return Task(
            description="Continuously update and refine the PRD based on feedback and changing requirements.",
            agent=agent,
            asynch_execution=True,
            context=context,
            expected_output="""A list of bullet points to describe respectively : 'Product name', 'Objectives', 'Features', 'User stories', 'Acceptance criteria'.
                        Example output:
                        'Product Name: Real-Time Collaboration Web App
                        Objectives: 
                        - Enable real-time document editing and collaboration.
                        - Provide seamless user experience across different devices.
                        Features:
                        - User Authentication and Profile Management.
                        - Real-time Document Editing with Version Control.
                        User Stories:
                        - As a user, I want to create and edit documents in real-time with my team.
                        - As a user, I want to receive notifications when someone comments on my document.
                        Acceptance Criteria:
                        - The application should allow multiple users to edit the same document simultaneously.
                        - Changes should be visible to all users in real-time without page refresh.'
            """
        )
    
    def review_code_task(self, agent, context):
        return Task(
            description="Continuously update and refine the PRD based on feedback and changing requirements.",
            agent=agent,
            asynch_execution=True,
            context=context,
            expected_output="""A list of bullet points to describe respectively : 'Product name', 'Objectives', 'Features', 'User stories', 'Acceptance criteria'.
                        Example output:
                        'Product Name: Real-Time Collaboration Web App
                        Objectives: 
                        - Enable real-time document editing and collaboration.
                        - Provide seamless user experience across different devices.
                        Features:
                        - User Authentication and Profile Management.
                        - Real-time Document Editing with Version Control.
                        User Stories:
                        - As a user, I want to create and edit documents in real-time with my team.
                        - As a user, I want to receive notifications when someone comments on my document.
                        Acceptance Criteria:
                        - The application should allow multiple users to edit the same document simultaneously.
                        - Changes should be visible to all users in real-time without page refresh.'
            """
        )

    def write_tasks_task(self, agent, context):
        return Task(
            description="Break down the project into manageable tasks and create detailed task descriptions.",
            agent=agent,
            asynch_execution=True,
            context=context,
            expected_output="""A list of tasks with descriptions, assignees, and due dates.
                        Example output:
                        'Task: Implement User Authentication
                        Description: Develop the user authentication module including login, registration, and password recovery.
                        Assignee: Engineer 1
                        Due Date: 2024-07-15'"""
        )
    
    def assign_tasks_task(self, agent, context):
        return Task(
            description="Allocate tasks to appropriate team members based on their skills and availability.",
            agent=agent,
            asynch_execution=True,
            context=context,
            expected_output="""A mapping of tasks to team members.
                        Example output:
                        'Task Assignment:
                        - Task: Implement User Authentication -> Engineer 1
                        - Task: Develop Real-Time Document Editing -> Engineer 2
                        - Task: Integrate Chat and Notifications -> Engineer 3'"""
        )

    def write_code_task(self, agent, instruction):
        return Task(
            description="Develop the software according to the specifications in the design documents.",
            agent=agent,
            asynch_execution=True,
            context=instruction,
            expected_output="""The code implementing the specified functionality, along with comments and test cases.
                        Example output:
                        'def authenticate_user(username, password):
                            user = get_user_from_db(username)
                            if user and check_password(user['password'], password):
                                return generate_token(user)
                            else:
                                raise AuthenticationError("Invalid credentials")'"""
        )
    
    def review_code_task(self, agent, context):
        return Task(
            description="Conduct code reviews to ensure that the implementation adheres to the design and meets quality standards.",
            agent=agent,
            asynch_execution=True,
            context=context,
            expected_output="""A review report detailing the findings and suggestions for improvement.
                        Example output:
                        'Code Review:
                        - The code follows the defined architecture and design patterns.
                        - Recommended refactoring the authentication module to enhance security.'"""
        )
    
    def debug_code_task(self, agent, context):
        return Task(
            description="Identify and fix bugs and issues in the code.",
            agent=agent,
            asynch_execution=True,
            context=context,
            expected_output="""A report of the bugs identified and the fixes applied.
                        Example output:
                        'Debugging:
                        - Fixed a bug causing session timeouts during peak usage.
                        - Identified and resolved a memory leak in the WebSocket connection handling.'"""
        )
    
    def write_tests_task(self, agent, context):
        return Task(
            description="Develop test cases and scenarios to validate the functionality and performance of the software.",
            agent=agent,
            asynch_execution=True,
            context=context,
            expected_output="""A set of test cases for the specified feature.
                        Example output:
                        'def test_authenticate_user():
                            assert authenticate_user('testuser', 'correctpassword') == expected_token
                            assert authenticate_user('testuser', 'wrongpassword') == AuthenticationError'"""
        )
    
    def run_tests_task(self, agent, context):
        return Task(
            description="Execute test cases, report defects, and verify fixes to ensure the software meets quality standards.",
            agent=agent,
            asynch_execution=True,
            context=context,
            expected_output="""A report of the test execution results, including identified defects and verification of fixes.
                        Example output:
                        'Test Results:
                        - All test cases passed for user authentication.
                        - Identified a bug in the real-time document editing feature causing data loss.'"""
        )
    







    
    

        

            
