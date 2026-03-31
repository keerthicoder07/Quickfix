### QuickFix

The app for electronics repair shop

### Installation

You can install this app using the [bench](https://github.com/frappe/bench) CLI:

```bash
cd $PATH_TO_YOUR_BENCH
bench get-app $URL_OF_THIS_REPO --branch develop
bench install-app quickfix
```

### Contributing

This app uses `pre-commit` for code formatting and linting. Please [install pre-commit](https://pre-commit.com/#installation) and enable it for this repository:

```bash
cd apps/quickfix
pre-commit install
```

Pre-commit is configured to use the following tools for checking and formatting your code:

- ruff
- eslint
- prettier
- pyupgrade

### CI

This app can use GitHub Actions for CI. The following workflows are configured:

- CI: Installs this app and runs unit tests on every push to `develop` branch.
- Linters: Runs [Frappe Semgrep Rules](https://github.com/frappe/semgrep-rules) and [pip-audit](https://pypi.org/project/pip-audit/) on every pull request.


### License

mit

Questions of A2
    What is Config file?
        The config file which are used to set the settings among the sites where we have the two types of config file

        site_config.json
            Where we can set the settings to that particular site and can maintain the version and other information separately to that particular site.
        
        common_site_config.json
            Where we can set the common settings which are applicable to all the sites globally.


    what breaks if you accidentally put a secret in common_site_config.json?
        Where every sites will access that data where even the production site users can access it which leads to the security risk,data leaks and data over writing which leads to the app crash.

    list the 4 processes bench start launches (web, worker, scheduler,socketio) and
    explain what happens to background jobs if the worker process crashes?

        Web-Handles the http request and web activities like api etc.
        Worker-Handles the background jobs in the redis queue.
        scheduler-Handles the Trigger scheduled jobs and cron jobs
        Socketio-Handles the realtime communication using websockets

        If the worker crashes the background jobs will remains in the job queue and will not execute

Questions of B1
    When a browser hits /api/method/quickfix.api.get_job_summary - what Python
    function handles this request and how does Frappe find it?
        In this scenario the python function executes and written the data in the json form and where the frappe finds the request using the module,class name and the function name and map the url to the handlers.
    
    When a browser hits /api/resource/Job Card/JC-2024-0001 - what happens differently compared to /api/method/?
        Where the first url returns the data of the doctype in the json with doctype name and document name and the second url which executes the custom python function by the developer.
    
    When a browser hits /track-job - which file/function handles it and why?
        The file named track-job.html or track-job.py and where the frappe expect the function get_context to render the content and where it check in the www folder since it is not any api methods or requests.

    Open your Frappe site in browser devtools. Find the X-Frappe-CSRF-Token in a
    POST request. Where does this value come from and what would happen if you
    omitted it? 
        The X-frappe-csrf token automatically created by the server during the login and store it in the server side and sent to the web browser through the cookies so whenever the user try to make post,put or delete action it validates the csrf token so we can block the malicious attacks if it is omitted where any other malicious users can done the post,put or delete actions.
    
    In bench console, run: import frappe; frappe.session.data and describe what it
    contains?
        In the session data where it contains the current user details like their unique session id and their name and what type of user and also contains the ip address and time stamps included with the csrf token
    
    With developer_mode: 1 - trigger a Python exception in one of your whitelisted
    methods. What does the browser receive?
        With this mode where browser recieves the traceback error in json and it displays the traceback the total error
    
    Set developer_mode: 0 - repeat. What does the browser receive now? Why is this
    important for production?
        With this mode where browser recieves the http error like internal server error because when the traceback display the user gets annoyed and also cannot find what's the problem so it is important in the production side.
    
    Where do production errors go if they are hidden from the browser?
        The production errors are still maintain in the error logs internally where we can also access through the error log doctype
    
    In a whitelisted method, call frappe.get_doc("Job Card", name) WITHOUT
    ignore_permissions. Then log in as a QF Technician user who is NOT assigned to
    that job. What error is raised and at what layer does Frappe stop the request?
        Where the frappe throws the user permission error that this user not have access to that particular resource and it stops at the document model layer
        after the execution of check_permission function.
    
    





