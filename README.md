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
    
Questions of B2
PART A
    Run: frappe.db.sql("SHOW TABLES LIKE '%Job%'") and list what you see. Explain
    the tab prefix convention.
        In [2]: frappe.db.sql("show tables like '%Job%'")
        Out[2]: (('tabJob Card',), ('tabScheduled Job Log',), ('tabScheduled Job Type',))

        So the tab prefix convention avoid the naming conflcits and give the easy identification to retrive the tables easily and helps orm to easilt map with doctype.
    
    Run: frappe.db.sql("DESCRIBE `tabJob Card`", as_dict=True) and list 5 column
    names you recognise from your DocType fields.
    
        In [3]: frappe.db.sql("describe `tabJob Card`",as_dict=True)
        Out[3]: 
        [{'Field': 'name',
        'Type': 'varchar(140)',
        'Null': 'NO',
        'Key': 'PRI',
        'Default': None,
        'Extra': ''},
        {'Field': 'creation',
        'Type': 'datetime(6)',
        'Null': 'YES',
        'Key': '',
        'Default': None,
        'Extra': ''},
        {'Field': 'modified',
        'Type': 'datetime(6)',
        'Null': 'YES',
        'Key': 'MUL',
        'Default': None,
        'Extra': ''},
        {'Field': 'modified_by',
        'Type': 'varchar(140)',
        'Null': 'YES',
        'Key': '',
        'Default': None,
        'Extra': ''},
        {'Field': 'owner',
        'Type': 'varchar(140)',
        'Null': 'YES',
        'Key': '',
        'Default': None,
        'Extra': ''},
        {'Field': 'docstatus',
        'Type': 'int(1)',
        'Null': 'NO',
        'Key': '',
        'Default': '0',
        'Extra': ''},
        {'Field': 'idx',
        'Type': 'int(8)',
        'Null': 'NO',
        'Key': '',
        'Default': '0',
        'Extra': ''},
        {'Field': 'amended_from',
        'Type': 'varchar(140)',
        'Null': 'YES',
        'Key': 'MUL',
        'Default': None,
        'Extra': ''},
        {'Field': '_user_tags',
        'Type': 'text',
        'Null': 'YES',
        'Key': '',
        'Default': None,
        'Extra': ''},
        {'Field': '_comments',
        'Type': 'text',
        'Null': 'YES',
        'Key': '',
        'Default': None,
        'Extra': ''},
        {'Field': '_assign',
        'Type': 'text',
        'Null': 'YES',
        'Key': '',
        'Default': None,
        'Extra': ''},
        {'Field': '_liked_by',
        'Type': 'text',
        'Null': 'YES',
        'Key': '',
        'Default': None,
        'Extra': ''},
        {'Field': 'customer_name',
        'Type': 'varchar(140)',
        'Null': 'YES',
        'Key': '',
        'Default': None,
        'Extra': ''},
        {'Field': 'customer_phone',
        'Type': 'varchar(140)',
        'Null': 'YES',
        'Key': '',
        'Default': None,
        'Extra': ''},
        {'Field': 'customer_email',
        'Type': 'varchar(140)',
        'Null': 'YES',
        'Key': '',
        'Default': None,
        'Extra': ''},
        {'Field': 'device_type',
        'Type': 'varchar(140)',
        'Null': 'YES',
        'Key': '',
        'Default': None,
        'Extra': ''},
        {'Field': 'device_brand',
        'Type': 'varchar(140)',
        'Null': 'YES',
        'Key': '',
        'Default': None,
        'Extra': ''},
        {'Field': 'device_model',
        'Type': 'varchar(140)',
        'Null': 'YES',
        'Key': '',
        'Default': None,
        'Extra': ''},
        {'Field': 'imei_or_serial',
        'Type': 'varchar(140)',
        'Null': 'YES',
        'Key': '',
        'Default': None,
        'Extra': ''},
        {'Field': 'problem_description',
        'Type': 'longtext',
        'Null': 'YES',
        'Key': '',
        'Default': None,
        'Extra': ''},
        {'Field': 'assigned_technician',
        'Type': 'varchar(140)',
        'Null': 'YES',
        'Key': '',
        'Default': None,
        'Extra': ''},
        {'Field': 'diagnosis_notes',
        'Type': 'longtext',
        'Null': 'YES',
        'Key': '',
        'Default': None,
        'Extra': ''},
        {'Field': 'estimated_cost',
        'Type': 'decimal(21,9)',
        'Null': 'NO',
        'Key': '',
        'Default': '0.000000000',
        'Extra': ''},
        {'Field': 'diagnosis_date',
        'Type': 'date',
        'Null': 'YES',
        'Key': '',
        'Default': None,
        'Extra': ''},
        {'Field': 'priority',
        'Type': 'varchar(140)',
        'Null': 'YES',
        'Key': '',
        'Default': 'Normal',
        'Extra': ''},
        {'Field': 'parts_total',
        'Type': 'decimal(21,9)',
        'Null': 'NO',
        'Key': '',
        'Default': '0.000000000',
        'Extra': ''},
        {'Field': 'labour_charge',
        'Type': 'decimal(21,9)',
        'Null': 'NO',
        'Key': '',
        'Default': '0.000000000',
        'Extra': ''},
        {'Field': 'final_amount',
        'Type': 'decimal(21,9)',
        'Null': 'NO',
        'Key': '',
        'Default': '0.000000000',
        'Extra': ''},
        {'Field': 'payment_status',
        'Type': 'varchar(140)',
        'Null': 'YES',
        'Key': '',
        'Default': 'Paid',
        'Extra': ''},
        {'Field': 'naming_series',
        'Type': 'varchar(140)',
        'Null': 'YES',
        'Key': '',
        'Default': None,
        'Extra': ''},
        {'Field': 'delivery_date',
        'Type': 'date',
        'Null': 'YES',
        'Key': '',
        'Default': None,
        'Extra': ''},
        {'Field': 'remarks',
        'Type': 'text',
        'Null': 'YES',
        'Key': '',
        'Default': None,
        'Extra': ''},
        {'Field': 'status',
        'Type': 'varchar(140)',
        'Null': 'YES',
        'Key': '',
        'Default': None,
        'Extra': ''}]

        The 5 column names i recognise are Technician name,parts used,labour charge,total amount,status.
    
PART D
    What are the three numeric values of docstatus and what state does each represent?
        The three numeric values of doc status are 0,1,2 and the each status represents
        0-Means the document is in draft state
        1-Means the document is in submitted state
        2-Means the document is in cancelled state
    Can you call doc.save() on a submitted document? What about doc.submit() on a
    cancelled one? Test in bench console and explain why?
        No, We cannot call doc.save() for the submitted document because we cannot edit even if we call without any changes it just return docname and its status.

        No, We cannot call doc.submit() for the cancelled document and it shows we cannot edit or submit the cancelled document and where we can amend that document and edit the fields which will stored with suffix number after the cancelled document name.
    
    Why would you see a "Document has been modified after you have opened it" error and how does Frappe prevent concurrent overwrites?
        This means another user is accessed and modified the things after you open so we can refresh or reload to get the latest version
        Frappe prevents the concurrent overwrites by checking the modified time of document and database modified time if it not matches it throws the error Document has been modified after you have opened it.

PART E
    Corrected version
    def validate(self):
        self.total=sum(r.amount for r in self.items)
    self.save() 
    # where if we call the save method inside validate it will cause the infinite loop because the document lifecycle of frappe during every call of save method it call validate function

    def on_submit(self):
        other=frappe.get_doc("Spare Part",self.part)
        other.stock_qty-=self.qty
        other.save()
        #where if we do the other.stock_qty-=self.qty during the each validation it will decrease the quantity which leads to the wrong data maintainence so we decrease only after the successful submission.


Questions of C1
    When you append a row to Job Card.parts_used and save, what 4 columns does
    Frappe automatically set on the child table row?
        When I append the row to the job card in the parts_used the frappe automatically set the 4 columns they are 
            Parent-Parent of the childtable
            parent type-Stores the type of the parent
            parent field-Stored the field name of the childtable in parent
            idx-It stores the row id
    What is the DB table name for the Part Usage Entry DocType?
        The Doctype Part usage entry will be stored with tab prefix as tab Part Usage Entry
    If you delete row at idx=2 and re-save, what happens to idx values of remaining
    rows?
        The frappe will automatically reoreder the idx values once the row id deleted and it always maintains the sequence in order.
    Rename one of your test Technician records using the Rename Document feature.Then check: does the assigned_technician field on linked Job Cards automaticallyupdate? Why or why not? What does "track changes" mean in this context?
        Yes the assigned_technician name will be update after the change sonce it is the link datatype which will always be with referential intergrity and the track changes mean where it track the changes in the field that happens in the particular document so we can see the change what happend old->new data
    Explain unique constraints: what is the difference between setting a field as "unique" in the DocType vs doing a frappe.db.exists() check in validate()?
        Setting the field as unique will make the changes in db where it will make the column as unique constraint but in db.exists() that check in the validate will not safe where it checks before the save so there is threat to the race condition so the unique method is safer than db.exists() in validate function.

Questions D2
    What is the issues in using frappe.get_all in a whitelisted method that is exposed to guests or low-privilege users. Explain it in the context of permission_query_conditions?
        While using the get_all in whitelistted method where it will not check any permissions and even give the data to any user and guests so where the hook function permission_query_conditions will check whetehr user

Questions of E1
    Call self.save() inside on_update and see to the issues of it and explain them in the same readme_internals. Correct the pattern and explain it.
        We cannot call self.save() in update where it creates the recursion where after update frappe calls save it also call on_update so if we use save again on_update it creates the infinite recursion so just write the things need in on_update and leave it frappe automatically saves during document lifecycle

Question of E3
Part A
    Write a comment block explaining: what is Method Resolution Order (MRO), and why
    calling super() is non-negotiable?
        MRO defines the order in which python looks in a class hireachy when custom job card inherits form job card python Mro decides which validate() to execute
        and calling super().validate() is non negotiable where it always has somw data and permission checks to maintain integrity
    
    Write a comment block explaining: when would you choose override_doctype_class
    over doc_events?
        override_doctype_class is used when you want to fully replace or extend the
    behavior of a DocType by subclassing its Python class. It gives complete control
    over lifecycle methods (validate, on_submit, on_cancel, etc.) and allows deep
    customization using inheritance.
        doc_events, on the other hand, is used to hook into specific events without
    modifying the original class. It is suitable for lightweight extensions such as
    triggering additional logic on certain events.

Part B
    Assume the Frappe core updates Job Card's validate() to add a new check. If you
    override_doctype_class and forget to update super() - what breaks? Write a test that catches this.
        When we forget to call the super() methon in validate where it will not check the core validations and when we override it with child class where only the child validation will execute and will not run the super.validation which leads to the data intergrity
    
    Explain in README_internals.md: why is doc_events safer than
    override_doctype_class for most use cases?
        Where the doc_events is more safer than override because it just work like an add-ons where it will check the core validations without fail but if we forget to call the super in the override class then it leads to the break of data and validations including permission checks so mostly we use the doc_events

Part C
    In the Spare Part controller, add an on_update method
    Which of the below pattern would you use and and explain why.
    doc = frappe.get_doc("QuickFix Settings", "QuickFix Settings")
    threshold = doc.low_stock_threshold
    threshold = frappe.db.get_value("QuickFix Settings", None,
    "low_stock_threshold")

        Here the frappe.db.get_value will perform well since it gets only one value but the get_doc where loads the whole document which slow down the process so the second method is better to use and since it is single doctype we can give the document field as None.

Questions of F1
    Register TWO validate handlers on Job Card - one in your main controller and one in doc_events. In README_internals.md: in what order do they run? What happens if both raise a frappe.ValidationError?
        In this scenario first the the controller validation will execute first and then doc_event hook will execute then and when the controller validation fails the doc_events will not execute and even if it pass and fails during the doc_event the it will not save that document and there is no chance to raise the error by both validations at same time so anyone can raise error where there it self execution will stop.
    
    Demonstrate: what happens when you register "*" AND a specific DocType handler
    for the same event? Do both run?
        Yes the both events also will execute and first the specific Dcotype handler will execute and the wildcard handlers will execute if any one of the handler throws the validation error then other handlers will not execute

Questions of F3
    app_include_js: a JS file loaded only for logged-in desk users
    web_include_js: a JS file loaded only for website/portal pages
    Explain in README_internals.md: what is the difference? When would you use
    each?
        Here the app_include_js will be hook only to the desk users and also visible only when user is logged in without login it will not visilble to the user
        For the website js hook which is like the public page where any user can see that page and visible to all users for example like landing page of website.
    
    doctype_js for Job Card, doctype_list_js for Job Card
    doctype_tree_js: not applicable here - explain in README what DocType would use
    a tree view and why
        The job card doctype is not a tree doctype where the tree structure has hierarchial so it is not applicable but where doctype_js and list view can be applicable since it is not single type doctype so we can have the list of documents
    Build cache-busting: explain what bench build --app quickfix does and why assets
    need cache-busting after JS changes
        After the changes in the js and css should be rebuild again in the application to show the new updated ui where the command bench build --app will create the new version of bundles files which is hashed file and where the assests need the cache busting after js changes to show the new and updated ui instead of showing older version
    
    Explain: what is the difference between a Jinja context available in Print Formats vs one available in Web Pages? Are they the same?
        The printable format is particularly for the document where we can use it to generate the pdf and print as our wish format like sales invoice scenario etc
        but the web pages are used to display the dynamic data and to create the website pages to render with dynamic data







