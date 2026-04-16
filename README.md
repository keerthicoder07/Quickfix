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

Questions of F4
    explain the difference between override_whitelisted_methods (hook-based, reversible, explicit) vs monkey patching (import-time, brittle, invisible). When would you use each?
        The override_whitelisted_methods are mostly used in the production where it just override the methods and we can override using the hook but monkey patching will just silentely uses the memory refernce of original during the runtime and which is unstable for the production and can only use for debugging and quick testing
    
    What happens if TWO apps both register override_whitelisted_methods for the same method? Write the answer.
        If two apps register override the last app's registered method only works because it only recently loaded and the first loaded and registered uses the original fucntion not the override method so the last app's override function will works.
    
    Explain about the Signature mismatch and not having exactly the same arguments
    as the original and in what case would you get a TypeError.
        The signature mismatch occurs when the custom function not matches the same arguments and default of original fucntion and the type error occurs when the value is sent with mismatch datatype that not expected by that function so we should give the argument values correctly as per the paramater
    
Questions of F5
    Explain fieldname collision risk: what happens if your Custom Field has the same fieldname as a field added by a future Frappe update?
        Fieldname collision occurs when a custom field uses the same fieldname as a
        field introduced later by Frappe or another app. Since fieldnames map directly
        to database columns, this leads to conflicts during migrations, causing errors
        such as duplicate column exceptions. To avoid this, custom fields should use
        unique prefixes (e.g., qf_) to ensure namespace isolation and future compatibility.
    Explain patching order: if Patch 1 creates a Custom Field and Patch 2 reads it, why must they be separate entries in patches.txt and never merged?
        Patches in Frappe are executed sequentially as listed in patches.txt. Each patch should perform a single, well-defined operation. If one patch depends on another (e.g., creating a Custom Field and then using it), they must be defined as separate entries. This is because schema changes may not be immediately available within the same execution context, and combining dependent operations in a single patch can lead to failures. Maintaining separate patches ensures proper execution order, dependency management, and migration stability.

Questions of G1
    What is the _qf_patched guard for? What breaks without it?
        The _qf_patched is used in the monkey patching to avoid the double or multiple patching by wrapping the same functionality again and again and without the guard it leads to the break down of execution,infinite run etc and it is hard ot debug also so the qf_patch guards that.
    
    Why is isolating patches in monkey_patches.py better than scattering them in
    __init__.py?
        When we keep the monkey patches it will be hidden and during every import or loading it will silently pathces and hard to debug so we use the separate monkey_patches.py which can be control and can maintain all the patches in the single file and easy to debug
    
    What is the correct escalation path: try doc_events first - then
    override_doctype_class - then override_whitelisted_methods - then monkey patch.Why is this the order?
        The correct escalation to first try the doc_events which can be easily implemented and safer method to handle next the override the doctype which give the full control of the doctype and prevetns the logic even during the update of core doctype and the third is some what risky sice it is external as whitelisted methods and last one is dangerous where it can breakdown the app so we mostly not use this monkey patch.so we ensures the safer->dangerous order.

Questions of H4
    when would a consultant use Client Script DocType vs an app developer use shipped JS? What are the risks of Client Script DocType in production?
        The consultant use the client script only during the sudden feature to be added as per client's priority and where we cannot do version control on it and it can break anytime and can also overriden accidentally but shipped js code will be save in the code and where we can test it and can modify it and maintain version control.
    
    Demonstrate the hiding fields vs permission security pitfall: add a JS field hide that hides customer_phone for non-managers - then show that an API call can still retrieve the field. Explain why hiding in JS is not a security measure.
        The hide fields will just will not show the details in the UI but they can still take form the api calls and cans till retrive the data from that field so we should write the permission conditions in the backend for real security

Questions of I1
    Demonstrate and explain the issues and solutions with respect to f-string SQL and the parameterized pattern.
        When we use the f -string in sql query ther is the threat for sql injection and also if we use single quotes in that variable where it shows error so we use the parameterized pattern which can be safe and take as data not as sql command 
    
    Add a EXPLAIN statement in bench console for your query - screenshot the result
    and identify if an index is being used on the status column
        Out[1]: 
        [{'id': 1,
        'select_type': 'SIMPLE',
        'table': 'tabJob Card',
        'type': 'ALL',
        'possible_keys': None,
        'key': None,
        'key_len': None,
        'ref': None,
        'rows': '2',
        'Extra': 'Using where'}]
        So here the index not used where the db scans all the record so if we use index it will be fast and gets the data faster by using index
    Add a proper index on Job Card.status by modifying the DocType JSON to include
    search_index: 1 on the status field
        Out[1]: 
        [{'id': 1,
        'select_type': 'SIMPLE',
        'table': 'tabJob Card',
        'type': 'range',
        'possible_keys': 'status_index',
        'key': 'status_index',
        'key_len': '563',
        'ref': None,
        'rows': '2',
        'Extra': 'Using index condition'}]
        so where in this we use the index it will speed up the process and search using the index not with where .

Questions of J1
    Putting a frappe.get_all() call inside the Jinja template directly?
        Initially it slow down the process because in each render it runs the db commands and also where the get_all will ignore all the permissions so any one can access the data without any permission conditions and it is hard to debug where it raises the wsgi error
    Pre-compute in before_print() and attach to self, then reference in template as
    doc.precomputed_field.
        yes it is better instead of we add in the jinja template because we can maintain all the logic in one end in server side so we dont want to switch to places to edit or check the logics and it is the easy way to work.

Questions of K1
    In README_internals.md: explain the 3 queue names (default, long, short) and when
    to use each
        Default-Which done the tasks which are with medium and normal mode where all the hooks and other default background jobs are run as default

        short-Which gives the high priority jobs like sending email and notifications where we can schedule these jobs using enqueue 

        long-Which can schedule using the enqueue which run the heavy load processes and can give the timeout to terminate to avoid running so long time without running other jobs
    
    Explain retry behavior: how many times does Frappe retry a failed background job by default?
        Frappe will not retry the background jobs by default where user should manually retry that and also where if it can retry defaulty there is a cause of infinite loop so where we can avoid the multiple retry using Idempotency and which is safer too.


Output of L1
    cookies for session
    http://quickfix-dev.localhost:8000/api/method/login
        sid
        71e2351254003176fbdfcfa2cd7cba8d7f5fdf02294b44d699195da0
        quickfix-dev.localhost
        /
        Wed, 22 Apr 2026 11:07:19 GMT
        true
        false
        system_user
        yes
        quickfix-dev.localhost
        /
        Session
        false
        false
        full_name
        Administrator
        quickfix-dev.localhost
        /
        Session
        false
        false
        user_id
        Administrator
        quickfix-dev.localhost
        /
        Session
        false
        false
        user_image
        quickfix-dev.localhost
        /
        Session
        false
        false
    
    GET /api/resource/Job Card - list Job Cards (use session cookie from browser)
    http://quickfix-dev.localhost:8000/api/resource/Job Card/
        {"data":[{"name":"JC-2026-00010"},{"name":"JC-2026-00011"},{"name":"JC-2026-00012"}]}
    
    GET /api/resource/Job Card/JC-0001 - single doc
    http://quickfix-dev.localhost:8000/api/resource/Job Card/JC-2026-00012
        {"data":{"name":"JC-2026-00012","owner":"Administrator","creation":"2026-04-13 13:32:52.852679","modified":"2026-04-13 17:55:42.292503","modified_by":"Administrator","docstatus":1,"idx":0,"custom_labour":"Labour","customer_name":"keerthi","customer_phone":"1234567890","device_type":"Smartphone","device_brand":"Xiamoi","device_model":"X12","problem_description":"<div class=\"ql-editor read-mode\"><p>ergbrgd</p></div>","assigned_technician":"TECH-0002","diagnosis_notes":"<div class=\"ql-editor read-mode\"><p>m,ml l</p></div>","estimated_cost":400.0,"diagnosis_date":"2026-04-11","priority":"Urgent","parts_total":150.0,"labour_charge":500.0,"final_amount":650.0,"payment_status":"Paid","delivery_date":"2026-04-13","status":"For Delivery","doctype":"Job Card","parts_used":[{"name":"nu06k1secc","owner":"Administrator","creation":"2026-04-13 13:32:52.852679","modified":"2026-04-13 17:55:42.292503","modified_by":"Administrator","docstatus":1,"idx":1,"part":"Sp-2026-00001","part_name":"Mic","unit_price":150.0,"quantity":1.0,"total_price":150.0,"parent":"JC-2026-00012","parentfield":"parts_used","parenttype":"Job Card","doctype":"Part Usage Entry"}]}}
    
    POST /api/resource/Spare Part - create a part
    http://quickfix-dev.localhost:8000/api/resource/Spare Part?part_name=speaker
    
        {"data":{"name":"Sp-2026-00002","owner":"Administrator","creation":"2026-04-15 14:53:48.205082","modified":"2026-04-15 14:53:48.205082","modified_by":"Administrator","docstatus":0,"idx":0,"part_name":"speaker","unit_cost":0.0,"selling_price":0.0,"stock_qty":0.0,"reorder_level":5.0,"is_active":1,"doctype":"Spare Part"}}

    PUT /api/resource/Spare Part/PART-0001 - update a field
    http://quickfix-dev.localhost:8000/api/resource/Spare Part/Sp-2026-00002?part_name=Mobile speaker
        {"data":{"name":"Sp-2026-00002","owner":"Administrator","creation":"2026-04-15 14:53:48.205082","modified":"2026-04-15 14:57:41.387670","modified_by":"Administrator","docstatus":0,"idx":0,"part_name":"Mobile speaker","unit_cost":0.0,"selling_price":0.0,"stock_qty":0.0,"reorder_level":5.0,"is_active":1,"doctype":"Spare Part"}}
    
    DELETE /api/resource/Spare Part/PART-0001 - delete it
    http://quickfix-dev.localhost:8000/api/resource/Spare Part/Sp-2026-00002
        {"data":"ok"}
    
CURL command with authorization with api secret key and value
    kee_frappe@keerthi-LOQ-15ARP9:~/frappe-bench$ curl http://quickfix-dev.localhost:8000/api/method/quickfix.api.generate_monthly_revenue_report?year=2026 -H "Authorization:token 0914831b8f1a4ae:ace766af6a4d41a"
{"message":{"status":"success","year":2026,"total_revenue":500.0}}
    

    
    what is the difference between session cookie auth and token
    auth? Which is appropriate for browser use and which for server-to-server?
        The session cookies are stored in the web browser to authorize the resources and method you access don't authorization for every request and response it is better for browser app and the token auth where we send during every request and response where it is stateless and where it suits for server to server request and response

Output of Task C
    curl "http://quickfix-dev.localhost:8000/api/method/quickfix.api.get_job_summary?job_card_name=JC-2026-00012" \
  -H "Authorization: token 0914831b8f1a4ae:ace766af6a4d41a"
{"message":{"name":"JC-2026-00012","customer_name":"keerthi","status":"For Delivery","estimated_cost":400.0,"creation":"2026-04-13 13:32:52.852679","today_date":"2026-04-15"}} //with serialization of date

Failed output
    kee_frappe@keerthi-LOQ-15ARP9:~/frappe-bench$ curl "http://quickfix-dev.localhost:8000/api/method/quickfix.api.get_job_summary?job_card_name=JC-2026-00015"   -H "Authorization: token 0914831b8f1a4ae:ace766af6a4d41a"{"message":{"error":"Not found"}}

Output of Task D
    kee_frappe@keerthi-LOQ-15ARP9:~/frappe-bench$ curl "http://quickfix-dev.localhost:8000/api/method/quickfix.api.get_job_by_phone?phone=1234567890" 
    {"message":{"name":"JC-2026-00013","status":"Delivered"}}

    kee_frappe@keerthi-LOQ-15ARP9:~/frappe-bench$ curl "http://quickfix-dev.localhost:8000/api/method/quickfix.api.get_job_by_phone?phone=1234567890" 
    {"message":{"name":"JC-2026-00013","status":"Delivered"}}

    kee_frappe@keerthi-LOQ-15ARP9:~/frappe-bench$ curl "http://quickfix-dev.localhost:8000/api/method/quickfix.api.get_job_by_phone?phone=1234567890" 
    {"message":{"error":"Too many requests.Try again later"}}

    Explain in README: what are the real risks of allow_guest=True endpoints? List 3
    specific attack vectors.
        In this scenario where every one can access the api methods without any rate limits and the three risk vectors are
            Enumeration Attack-user can try multiple inputs to get the valid data
            
            DOS(Denial of service)-where the guest user can send thousands of request which will affect the server and leads to the crash

            Data Scraping-Where guest user can scrap mutiple data without any permissions
        

    


    


    
    
    








