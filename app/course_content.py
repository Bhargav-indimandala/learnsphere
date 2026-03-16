# Full rich-text content for every course.
# Each entry: (slug, what_you_learn, requirements, overview_html)

COURSE_CONTENT = {
"Python for Beginners": {
"what_you_learn": [
    "Write clean Python code using variables, loops, and functions",
    "Understand object-oriented programming with classes and inheritance",
    "Handle files, exceptions, and modules like a professional",
    "Build small real-world projects from day one",
    "Read and debug other people's Python code confidently",
    "Prepare for intermediate topics like web development and data science",
],
"requirements": [
    "No prior programming experience needed",
    "A computer with internet access (Windows, Mac, or Linux)",
    "Python 3.x installed (free — instructions provided in Week 1)",
    "2–3 hours per week of study time",
],
"overview": """
<p>Python is consistently ranked the world's most popular programming language, and for good reason — it reads almost like English, runs everywhere, and powers everything from Instagram to NASA's space missions.</p>

<p>This course is built for <strong>complete beginners</strong>. You don't need to know anything about programming to start. We begin at absolute zero and build up steadily, so every concept is introduced with plain-English explanations before a single line of code appears.</p>

<h4>What makes this course different?</h4>
<p>Most beginner Python courses dump syntax at you and hope it sticks. We take the opposite approach: every topic is taught through a small, satisfying project. By the end of Week 2 you'll have built a number-guessing game. By Week 4 you'll have a working to-do app with classes. By Week 6 you'll have a file-based data logger you built yourself.</p>

<h4>What you'll build</h4>
<ul>
  <li>A temperature converter and calculator (Week 1)</li>
  <li>A text-based number guessing game (Week 2)</li>
  <li>A contact book using functions and dictionaries (Week 3)</li>
  <li>A Student class with grades and GPA tracking (Week 4)</li>
  <li>A CSV-based expense tracker with error handling (Week 5)</li>
  <li>A capstone project of your choice (Week 6)</li>
</ul>

<h4>Instructor approach</h4>
<p>Dr. Sarah Chen has taught Python to over 40,000 students across university and online settings. Her method: short explanations, immediate exercises, frequent code review. Lessons are designed to be completed in under 45 minutes each.</p>
""",
},

"Data Science Fundamentals": {
"what_you_learn": [
    "Manipulate and clean real-world datasets using pandas",
    "Perform numerical computing with NumPy arrays",
    "Create publication-quality charts with Matplotlib and Seaborn",
    "Apply linear and logistic regression models",
    "Evaluate models using cross-validation, precision, recall, and F1",
    "Build an end-to-end ML pipeline from raw data to predictions",
],
"requirements": [
    "Basic Python knowledge (variables, loops, functions)",
    "High-school level statistics (mean, variance) is helpful but not required",
    "Jupyter Notebook or VS Code with Python extension",
    "4–5 hours per week",
],
"overview": """
<p>Data science is the skill that turns raw numbers into decisions. This course takes you from "I know Python" to "I can build and evaluate a machine learning model" in eight focused weeks.</p>

<p>You'll work with <strong>real datasets</strong> throughout — housing prices, customer churn, medical records, financial time series. No toy examples. Every technique is introduced in context so you understand not just the how, but the why.</p>

<h4>Week-by-week breakdown</h4>
<p><strong>Weeks 1–2</strong> cover the two pillars of numerical Python: NumPy for fast array operations and pandas for structured data. You'll learn how to load, inspect, clean, merge, group, and reshape data — the skills that take up 70% of a data scientist's actual work.</p>

<p><strong>Week 3</strong> is entirely visualisation. You'll learn to choose the right chart for the story you're telling, and produce graphs polished enough to put in a report or presentation.</p>

<p><strong>Week 4</strong> introduces statistical thinking: distributions, central tendency, correlation, and hypothesis testing. These concepts underpin every ML algorithm you'll use later.</p>

<p><strong>Weeks 5–7</strong> cover the core supervised learning toolkit: linear regression, logistic regression, decision trees, random forests, and support vector machines — using scikit-learn throughout.</p>

<p><strong>Week 8</strong> is a capstone: you pick a dataset, define a prediction problem, build a full pipeline, and present your results with charts and metrics.</p>

<h4>Tools covered</h4>
<ul>
  <li>Python 3, Jupyter Notebooks</li>
  <li>NumPy, pandas, Matplotlib, Seaborn</li>
  <li>scikit-learn (the industry-standard ML library)</li>
  <li>Google Colab (so nothing needs installing locally)</li>
</ul>
""",
},

"Web Development with Flask": {
"what_you_learn": [
    "Build and structure a full Flask web application from scratch",
    "Design and query SQLite databases using raw SQL",
    "Implement user authentication with hashed passwords and sessions",
    "Create a fully documented REST API with JSON responses",
    "Write unit and integration tests with pytest",
    "Deploy a live Flask app to a cloud server",
],
"requirements": [
    "Python fundamentals (functions, classes, dictionaries)",
    "Basic understanding of how the web works (HTTP, browsers)",
    "A terminal / command line you're comfortable opening",
    "5–6 hours per week",
],
"overview": """
<p>Flask is the web framework of choice for developers who want to understand exactly what their code is doing. Unlike larger frameworks that hide complexity behind magic, Flask puts you in control — which means you learn more and build faster once you understand the pieces.</p>

<p>This course is structured around a single evolving project: a full-featured course platform (much like the one you're using right now). You'll start with a "Hello World" route and finish with a deployed, tested web application complete with authentication, a REST API, and a database.</p>

<h4>What you'll build, week by week</h4>

<p><strong>Weeks 1–2: Flask fundamentals.</strong> Routing, URL parameters, the request/response cycle, Blueprints for code organisation, Jinja2 templating, static files. You'll build the skeleton of your project here.</p>

<p><strong>Week 3: Forms and validation.</strong> HTML forms, form handling in Flask, server-side validation, flash messages, redirects. You'll add a working contact form and admin panel.</p>

<p><strong>Week 4: Databases.</strong> SQLite with Python's built-in sqlite3 module. Schema design, migrations, CRUD operations, relationships between tables. You'll build the full data layer.</p>

<p><strong>Week 5: Authentication.</strong> Password hashing (PBKDF2), sessions, login required decorators, admin vs regular users. Secure by design from the start.</p>

<p><strong>Week 6: REST APIs.</strong> JSON responses, status codes, request parsing, API versioning. You'll build a complete API layer on top of your existing app.</p>

<p><strong>Week 7: Testing.</strong> pytest fundamentals, test client, fixtures, testing views and routes, coverage reports. You'll write tests for everything you've built.</p>

<p><strong>Weeks 8–9: Frontend and deployment.</strong> CSS organisation, responsive design basics, environment variables, gunicorn, and deploying to a Linux VPS or cloud platform.</p>

<p><strong>Week 10: Capstone.</strong> Extend your project with a feature of your choice — a search engine, file uploads, WebSocket notifications, or anything else that interests you.</p>
""",
},

"Machine Learning A-Z": {
"what_you_learn": [
    "Understand the mathematical foundations of popular ML algorithms",
    "Implement and tune models for classification, regression, and clustering",
    "Build and train neural networks using PyTorch",
    "Design convolutional networks for image classification",
    "Build sequence models (RNNs, LSTMs) for time series and NLP",
    "Apply reinforcement learning to simple game environments",
],
"requirements": [
    "Python proficiency (classes, list comprehensions, libraries)",
    "Linear algebra basics (vectors, matrices, dot products)",
    "Calculus basics (derivatives, chain rule) — a refresher is provided",
    "Completion of Data Science Fundamentals or equivalent experience",
    "A machine with a GPU is helpful but not required (Colab provided)",
],
"overview": """
<p>This is the most comprehensive machine learning course on the platform. Over 12 weeks you'll go from understanding gradient descent to training your own neural networks, and from basic clustering to implementing a Q-learning agent.</p>

<p>The course is designed for people who don't just want to call <code>model.fit()</code> — they want to understand <em>why</em> it works. Every algorithm is first derived mathematically (at an accessible level), then implemented from scratch in NumPy before being used via a library. This approach builds intuition that makes you a better ML practitioner for life.</p>

<h4>Part 1: Foundations (Weeks 1–2)</h4>
<p>The ML mindset, the bias-variance tradeoff, train/validation/test splits, cross-validation, gradient descent from scratch, regularisation (L1 and L2). You'll implement linear regression in pure NumPy before ever touching scikit-learn.</p>

<h4>Part 2: Supervised Learning (Weeks 3–4)</h4>
<p>Decision trees and random forests, gradient boosting (XGBoost), support vector machines, k-nearest neighbours. Feature engineering, handling imbalanced classes, hyperparameter tuning with grid search and random search.</p>

<h4>Part 3: Unsupervised Learning (Weeks 5–6)</h4>
<p>K-means and hierarchical clustering, dimensionality reduction (PCA, t-SNE), anomaly detection, Gaussian mixture models. Applied to customer segmentation and image compression.</p>

<h4>Part 4: Deep Learning (Weeks 7–10)</h4>
<p>PyTorch from scratch: tensors, autograd, building neural networks with <code>nn.Module</code>. Convolutional networks for image classification (CIFAR-10). Recurrent networks and LSTMs for sentiment analysis and time series forecasting.</p>

<h4>Part 5: Reinforcement Learning & Capstone (Weeks 11–12)</h4>
<p>The RL framework: agents, environments, rewards, policies. Q-learning, Deep Q-Networks (DQN) applied to OpenAI Gym. Capstone: build and document a complete ML project of your choosing.</p>
""",
},

"JavaScript & React": {
"what_you_learn": [
    "Master modern JavaScript (ES6+): arrow functions, destructuring, modules, async/await",
    "Manipulate the DOM and handle browser events confidently",
    "Build interactive UIs with React functional components and hooks",
    "Manage application state with useState, useReducer, and Context",
    "Fetch data from REST APIs and handle loading/error states",
    "Write unit tests with Jest and React Testing Library",
],
"requirements": [
    "Basic HTML and CSS knowledge",
    "No JavaScript experience required — we start from scratch",
    "A modern browser (Chrome or Firefox)",
    "VS Code with the ES7 React snippets extension",
],
"overview": """
<p>JavaScript is the only language that runs natively in every web browser, and React is the library that the world's most-used websites — Facebook, Instagram, Airbnb, Netflix — are built on. Together they're the most in-demand frontend skill stack you can learn.</p>

<p>This course takes a project-driven approach. You won't spend weeks reading about JavaScript before writing any. By the end of Week 1 you'll have built an interactive quiz app. By Week 5 you'll be building full React applications with state, routing, and live API data.</p>

<h4>JavaScript deep-dive (Weeks 1–3)</h4>
<p>We cover modern JavaScript properly: not just the basics, but the patterns that appear constantly in professional code. Closures, prototypes, the event loop, promises, async/await, modules, and the newer ES2022+ features. You'll understand <em>why</em> JavaScript behaves the way it does, which makes debugging vastly easier.</p>

<p>Week 2 focuses on the DOM: selecting elements, responding to events, updating content dynamically, building a drag-and-drop list from scratch. Week 3 covers asynchronous programming — the most confusing part of JavaScript for beginners — with a thorough treatment of the event loop, callbacks, promises, and async/await.</p>

<h4>React (Weeks 4–7)</h4>
<p><strong>Week 4</strong> introduces React: JSX, components, props, and the mental model of "UI as a function of state". <strong>Week 5</strong> covers hooks in depth: useState, useEffect, useRef, useMemo, useCallback, and building custom hooks. <strong>Week 6</strong> adds React Router for multi-page apps and introduces global state with Context API. <strong>Week 7</strong> ties it together: fetching from a public API, handling loading/error states, building a polished data-driven application.</p>

<h4>Testing (Week 8)</h4>
<p>Unit testing with Jest, component testing with React Testing Library, and end-to-end testing concepts. Deploying to Vercel or Netlify with CI via GitHub Actions.</p>
""",
},

"SQL & Database Design": {
"what_you_learn": [
    "Write SQL queries from simple SELECTs to complex multi-table JOINs",
    "Design normalised relational database schemas",
    "Optimise slow queries using indexes and EXPLAIN",
    "Use window functions, CTEs, and subqueries for advanced analysis",
    "Understand transactions, ACID properties, and isolation levels",
    "Apply schema design patterns used in production systems",
],
"requirements": [
    "No prior database experience needed",
    "Basic logical thinking (if/then, comparing values)",
    "DB Browser for SQLite (free) or PostgreSQL installed",
],
"overview": """
<p>SQL has been around since 1974 and it's not going anywhere. It's the lingua franca of data — every analyst, backend developer, and data scientist needs it. This course builds a foundation that will serve you across SQLite, PostgreSQL, MySQL, and any other relational database.</p>

<h4>Week 1: SQL fundamentals</h4>
<p>SELECT, FROM, WHERE, ORDER BY, LIMIT. Filtering with AND/OR/NOT, pattern matching with LIKE, working with NULLs. You'll query a real e-commerce dataset from the very first lesson.</p>

<h4>Week 2: Joins and aggregation</h4>
<p>INNER, LEFT, RIGHT, and FULL OUTER JOINs with visual diagrams for each. GROUP BY, HAVING, COUNT, SUM, AVG, MIN, MAX. Writing queries that answer real business questions: "Which products generate the most revenue?", "Which customers haven't ordered in 90 days?"</p>

<h4>Week 3: Schema design</h4>
<p>Entity-relationship modelling, the three normal forms (1NF, 2NF, 3NF), when to denormalise for performance, primary and foreign keys, constraints, and referential integrity. You'll design a complete schema for a social media application.</p>

<h4>Week 4: Performance</h4>
<p>How databases execute queries, what indexes are and how B-tree indexes work, using EXPLAIN/EXPLAIN ANALYZE to diagnose slow queries, composite indexes, covering indexes, and the common query patterns that kill performance.</p>

<h4>Week 5: Advanced SQL and transactions</h4>
<p>Window functions (ROW_NUMBER, RANK, LAG, LEAD, running totals), Common Table Expressions (CTEs), recursive CTEs, transactions and ACID properties, isolation levels and concurrency issues, and an introduction to stored procedures.</p>
""",
},

"DevOps & CI/CD": {
"what_you_learn": [
    "Write Bash scripts to automate repetitive server tasks",
    "Build, run, and compose multi-container applications with Docker",
    "Set up automated CI/CD pipelines using GitHub Actions",
    "Deploy to Kubernetes clusters and understand its core primitives",
    "Monitor applications with Prometheus and Grafana",
    "Apply infrastructure-as-code principles with real tools",
],
"requirements": [
    "Comfortable using the Linux terminal (cd, ls, grep, ssh)",
    "Basic knowledge of any backend programming language",
    "A GitHub account (free)",
    "Docker Desktop installed (free for personal use)",
],
"overview": """
<p>The gap between writing code and shipping it reliably at scale is what DevOps bridges. This course teaches you the tools, mindset, and workflows that allow small teams to deploy dozens of times per day with confidence.</p>

<h4>Week 1: Linux and shell scripting</h4>
<p>The Linux filesystem, permissions, processes, and networking tools every developer needs. Writing real Bash scripts: loops, conditionals, functions, cron jobs, and piping commands together. By the end of the week you'll have automated your first server setup.</p>

<h4>Weeks 2–3: Docker</h4>
<p>What containers are and why they solved a genuine problem. Writing Dockerfiles, building images, running containers, persisting data with volumes, exposing ports. Week 3 introduces Docker Compose for orchestrating multi-service apps (web + database + cache) with a single command.</p>

<h4>Weeks 4–5: GitHub Actions CI/CD</h4>
<p>What continuous integration means in practice. Writing workflows that automatically run tests on every pull request. Adding deployment steps: build a Docker image, push to a registry, and deploy to a server — all triggered by a git push. You'll set up a complete pipeline for a real application.</p>

<h4>Week 6: Kubernetes</h4>
<p>Why Kubernetes exists and what problems it solves. Core concepts: pods, deployments, services, configmaps, secrets, and namespaces. Deploying your containerised app to a local k8s cluster (kind or minikube) and understanding what happens when a pod crashes.</p>

<h4>Weeks 7–8: Cloud, monitoring, and capstone</h4>
<p>Deploying to AWS EC2 or GCP Compute Engine. Setting up Prometheus for metrics scraping and Grafana for dashboards. Alerting on error rates and latency. Capstone: build a complete CI/CD pipeline for an application of your choice, including infrastructure provisioning.</p>
""",
},

"Cybersecurity Fundamentals": {
"what_you_learn": [
    "Think like an attacker to build stronger defences",
    "Understand how common web vulnerabilities (SQLi, XSS, CSRF) work and how to fix them",
    "Use industry tools: Nmap, Burp Suite, Wireshark, and Metasploit",
    "Apply cryptographic principles: symmetric, asymmetric, hashing, TLS",
    "Perform network scanning and enumeration in a legal lab environment",
    "Write an incident response plan and conduct a basic forensic investigation",
],
"requirements": [
    "Basic networking knowledge (what is an IP address, what is TCP/IP)",
    "Comfortable with the Linux command line",
    "A laptop that can run VirtualBox or VMware (8GB RAM minimum)",
    "Commitment to only apply these skills ethically and legally",
],
"overview": """
<p>Cybersecurity is one of the fastest-growing fields in technology, and this course gives you a serious foundation — not just theory, but hands-on labs in a safe, legal environment. Every technique taught here is used by professional penetration testers and security analysts every day.</p>

<blockquote style="border-left:3px solid var(--border);padding-left:1rem;color:var(--muted);margin:1rem 0;"><em>Important: Everything in this course is taught for defensive and educational purposes. All labs use isolated virtual machines you control. Using these techniques against systems you don't own is illegal.</em></blockquote>

<h4>Week 1: The security mindset</h4>
<p>The CIA triad (Confidentiality, Integrity, Availability). Threat modelling: how to systematically identify what could go wrong in a system. The OWASP Top 10. Setting up your lab: Kali Linux in VirtualBox, a vulnerable target VM (DVWA and Metasploitable).</p>

<h4>Weeks 2–3: Networking and cryptography</h4>
<p>TCP/IP in depth, packet capture with Wireshark, DNS, ARP, and common network attacks. Then: symmetric encryption (AES), asymmetric encryption (RSA), hashing (SHA-256), digital signatures, TLS handshake, certificate authorities. Understanding how HTTPS actually works.</p>

<h4>Week 4: Web application security</h4>
<p>SQL injection — finding it, exploiting it, and preventing it. Cross-site scripting (XSS): reflected, stored, and DOM-based. CSRF: how it works and why CSRF tokens stop it. Authentication flaws, session fixation, and insecure direct object references. Using Burp Suite to intercept and modify HTTP traffic.</p>

<h4>Weeks 5–6: Network reconnaissance and exploitation</h4>
<p>Information gathering with Nmap, Shodan, and OSINT. Vulnerability scanning with Nessus/OpenVAS. Introduction to exploitation with Metasploit — targeting your own lab machines only. Post-exploitation basics: privilege escalation, persistence, pivoting.</p>

<h4>Weeks 7–8: Defence and hardening</h4>
<p>Hardening Linux servers, firewall rules with iptables/ufw, intrusion detection with Snort, log analysis, SIEM concepts. Writing a security policy and incident response runbook.</p>

<h4>Week 9: Capstone CTF</h4>
<p>A capture-the-flag challenge against a purpose-built vulnerable machine. Find and exploit vulnerabilities, escalate privileges, and capture flags — then write a professional penetration test report.</p>
""",
},

"iOS Development with Swift": {
"what_you_learn": [
    "Write idiomatic Swift using optionals, closures, protocols, and generics",
    "Build production-quality UIs entirely in SwiftUI",
    "Manage app state with @State, @Binding, @ObservedObject, and @EnvironmentObject",
    "Fetch and decode JSON from REST APIs using URLSession",
    "Persist data locally with UserDefaults, FileManager, and CoreData",
    "Prepare and submit an app to the App Store",
],
"requirements": [
    "A Mac running macOS 13 (Ventura) or later",
    "Xcode 15 installed (free from the Mac App Store)",
    "No prior iOS or Swift experience needed",
    "An Apple Developer account (free tier is sufficient for most of the course)",
],
"overview": """
<p>Swift is one of the most expressive, safe, and fast programming languages in existence today — and SwiftUI makes building beautiful iOS apps more accessible than ever. This course takes you from zero to App Store in ten focused weeks.</p>

<h4>Weeks 1–2: Swift language mastery</h4>
<p>Unlike courses that skim the language to get to UI quickly, we invest two weeks in Swift fundamentals — because shaky foundations cause pain later. You'll cover: value types vs reference types, optionals and safe unwrapping, closures, protocols, extensions, generics, and error handling. You'll write dozens of short programs to cement each concept.</p>

<h4>Week 3: SwiftUI basics</h4>
<p>The declarative paradigm: describing what your UI should look like rather than imperative commands. Views, modifiers, stacks (HStack, VStack, ZStack), Lists, NavigationStack, and the preview canvas. You'll build a fully designed profile card and a settings screen.</p>

<h4>Week 4: Data flow</h4>
<p>@State for local state, @Binding for parent-child communication, @ObservableObject and @ObservedObject for shared state, @EnvironmentObject for app-wide data. Building a complete task manager app that demonstrates each pattern.</p>

<h4>Week 5: Networking</h4>
<p>URLSession for HTTP requests, async/await in Swift, Codable and JSON decoding, error handling in network calls. Building a weather app that fetches live data from a public API.</p>

<h4>Weeks 6–7: Local data and advanced UI</h4>
<p>UserDefaults for simple persistence, FileManager for documents, CoreData for relational local data with a full CRUD example. Animations with withAnimation and .transition, gesture recognisers, custom shapes, and advanced list features.</p>

<h4>Weeks 8–9: Notifications and App Store</h4>
<p>Push notifications with APNs, local notifications, deep linking. Code signing, provisioning profiles, TestFlight beta testing, App Store Connect, screenshots, metadata, and the review process.</p>
""",
},

"UI/UX Design Fundamentals": {
"what_you_learn": [
    "Apply the double-diamond design process to any product problem",
    "Conduct user interviews and synthesise findings into actionable insights",
    "Create low and high-fidelity wireframes using Figma",
    "Build interactive prototypes and conduct usability tests",
    "Apply typography, colour theory, and layout principles professionally",
    "Produce a portfolio case study ready to show in job interviews",
],
"requirements": [
    "No design experience required",
    "A laptop or desktop (Mac or Windows)",
    "Figma account (free tier is sufficient)",
    "Curiosity about why products feel easy or frustrating to use",
],
"overview": """
<p>Good design is not decoration — it's problem solving. This course teaches you how professional designers think and work, from the very first moment of understanding a problem to the final usability test that proves the solution works.</p>

<h4>Week 1: Design thinking</h4>
<p>The double-diamond framework: Discover → Define → Develop → Deliver. Design thinking vs. design doing. Anatomy of a good design brief. You'll analyse three products you use every day and identify what makes them succeed or fail.</p>

<h4>Week 2: User research</h4>
<p>Why you can't trust your own assumptions. Interview techniques: open questions, the "five whys", avoiding leading questions. Affinity mapping and synthesis. Building user personas and journey maps. You'll interview three real people and synthesise your findings into a design direction.</p>

<h4>Week 3: Wireframing</h4>
<p>Information architecture: card sorting, sitemaps, user flows. Low-fidelity sketching on paper first (why pixels too early kills good ideas). Moving into Figma for mid-fidelity wireframes. UI patterns and when to use them: navigation, forms, cards, modals, empty states.</p>

<h4>Week 4: Figma and high-fidelity design</h4>
<p>Figma fundamentals: frames, auto layout, components, variants, and design tokens. Typography in practice: scale, hierarchy, line height, and pairing fonts. Colour: hue, saturation, value, accessible contrast ratios (WCAG AA/AAA), building a colour palette. You'll design a complete three-screen app in Figma.</p>

<h4>Week 5: Usability testing</h4>
<p>Building a clickable prototype in Figma. Writing a test script. Conducting moderated usability tests (in person and remote). Analysing findings and prioritising changes. Iterating your designs based on real user feedback.</p>

<h4>Week 6: Portfolio case study</h4>
<p>Structuring a design case study: problem, research, process, solution, outcomes. Writing about design for a technical and non-technical audience. Presenting your work confidently. You'll finish with a complete, shareable case study.</p>
""",
},

"Cloud Computing with AWS": {
"what_you_learn": [
    "Navigate the AWS console and CLI confidently",
    "Launch and manage EC2 instances, security groups, and Elastic IPs",
    "Store and serve files with S3, CloudFront, and lifecycle policies",
    "Build serverless functions with Lambda and API Gateway",
    "Design highly available architectures using RDS, Auto Scaling, and Load Balancers",
    "Pass the AWS Solutions Architect Associate exam",
],
"requirements": [
    "Basic understanding of Linux and networking (HTTP, DNS, firewalls)",
    "An AWS account (free tier covers most labs — estimated cost under $5 total)",
    "Familiarity with at least one programming language",
    "No prior cloud experience required",
],
"overview": """
<p>Amazon Web Services powers roughly a third of the entire internet. Whether you're a developer, architect, or engineer, understanding AWS has become a baseline expectation at most technology companies. This course prepares you both to use AWS effectively and to pass the AWS Solutions Architect Associate certification.</p>

<h4>Week 1: AWS foundations</h4>
<p>The cloud computing model (IaaS, PaaS, SaaS). AWS global infrastructure: regions, availability zones, and edge locations. The AWS console and CLI. IAM: users, groups, roles, and policies. The principle of least privilege. Setting up a secure root account and creating your first IAM user.</p>

<h4>Week 2: Compute</h4>
<p>EC2 instance types and pricing models (on-demand, reserved, spot). AMIs and launch templates. Security groups as stateful firewalls. Elastic IPs and key pairs. Lambda: building serverless functions in Python, triggers, environment variables, and the execution model.</p>

<h4>Week 3: Storage</h4>
<p>S3 bucket creation, policies, and versioning. Storage classes and cost optimisation. Hosting a static website on S3. CloudFront CDN: distributions, origins, cache behaviours, and HTTPS. EBS volumes, snapshots, and when to use EFS instead.</p>

<h4>Week 4: Databases</h4>
<p>RDS: managed relational databases (PostgreSQL, MySQL), Multi-AZ for high availability, read replicas for performance. DynamoDB: the NoSQL model, partition keys and sort keys, on-demand vs provisioned capacity, and when to choose NoSQL over relational.</p>

<h4>Weeks 5–6: Networking and security</h4>
<p>VPCs from scratch: subnets, route tables, internet gateways, NAT gateways. Public vs private subnets. Network ACLs vs security groups. VPN and Direct Connect. AWS WAF, Shield, and GuardDuty. Encryption at rest and in transit.</p>

<h4>Weeks 7–9: Architecture patterns</h4>
<p>Application Load Balancers and target groups. Auto Scaling groups with launch templates. SQS for decoupling services. SNS for notifications. CloudWatch metrics, logs, alarms, and dashboards. Well-Architected Framework: the five pillars.</p>

<h4>Week 10: Exam prep and capstone</h4>
<p>Full mock exam with explanations. Three architecture scenario walkthroughs. Capstone: design and deploy a three-tier web application (frontend on CloudFront/S3, API on Lambda/API Gateway, data on RDS) with monitoring and alerting.</p>
""",
},

"Blockchain & Web3": {
"what_you_learn": [
    "Explain how blockchains achieve consensus and why they're tamper-resistant",
    "Write, test, and deploy Solidity smart contracts to Ethereum testnets",
    "Interact with contracts using ethers.js from a web frontend",
    "Understand and implement common smart contract patterns (ERC-20, ERC-721)",
    "Identify and mitigate common smart contract vulnerabilities (reentrancy, overflow)",
    "Build and deploy a simple decentralised application (dApp) end to end",
],
"requirements": [
    "JavaScript proficiency (ES6+, async/await, npm)",
    "Basic understanding of how HTTP APIs work",
    "MetaMask browser extension installed",
    "Node.js 18+ installed",
],
"overview": """
<p>Blockchain technology promises to reshape finance, identity, ownership, and governance. This course cuts through the hype to give you a rigorous, engineer-level understanding of how blockchains actually work — and the practical skills to build on them.</p>

<h4>Week 1: Blockchain fundamentals</h4>
<p>What problem blockchain solves: the double-spend problem and trust without intermediaries. Hash functions and why they're the building block of blockchains. Merkle trees. Proof of Work vs Proof of Stake. How a block is validated and added to the chain. We'll implement a tiny blockchain in JavaScript to make these concepts concrete.</p>

<h4>Week 2: Ethereum deep dive</h4>
<p>Ethereum vs Bitcoin: accounts, not UTXOs. The EVM (Ethereum Virtual Machine): opcodes, gas, and the stack. Wallets, private keys, and addresses. Transaction structure. MetaMask setup. Connecting to testnets (Sepolia) with free test ETH.</p>

<h4>Weeks 3–4: Solidity</h4>
<p>Solidity syntax: types, functions, modifiers, events, and error handling. Contract structure and the deployment lifecycle. Mappings and arrays. The msg object. Payable functions and Ether transfers. Writing, compiling, and deploying your first token contract.</p>

<h4>Week 5: Testing and patterns</h4>
<p>Testing with Hardhat and Chai: unit tests for every function, testing reverts, simulating time. Gas optimisation patterns. ERC-20 (fungible tokens) and ERC-721 (NFTs) standards: implementing both from scratch, then using OpenZeppelin's audited implementations.</p>

<h4>Week 6: dApp frontend</h4>
<p>Connecting a React frontend to an Ethereum wallet using ethers.js. Reading contract state, sending transactions, listening for events. Building a complete token dashboard: balances, transfers, transaction history.</p>

<h4>Weeks 7–8: DeFi and security</h4>
<p>How AMMs (Uniswap), lending protocols (Aave), and stablecoins work under the hood. Common vulnerabilities: reentrancy attacks (the DAO hack), integer overflow, access control failures, oracle manipulation. How to audit your own contracts. Formal verification introduction. Capstone: build and deploy a complete, tested dApp.</p>
""",
},

"Statistics & Probability": {
"what_you_learn": [
    "Summarise and describe data using descriptive statistics",
    "Apply probability rules and reason under uncertainty",
    "Work with the most important probability distributions",
    "Conduct and interpret hypothesis tests (t-tests, chi-squared, ANOVA)",
    "Apply Bayes' theorem and understand Bayesian vs frequentist thinking",
    "Run regression analyses and understand their assumptions",
],
"requirements": [
    "High-school algebra (solving equations, working with fractions)",
    "No calculus required — we provide intuitive explanations throughout",
    "Python with NumPy and SciPy installed (or Google Colab)",
    "Curiosity about how we know what we know from data",
],
"overview": """
<p>Statistics is the science of learning from data. It underpins machine learning, clinical trials, A/B testing, polling, finance, and virtually every field that makes decisions based on evidence. Yet most people's statistics education stops at mean and standard deviation. This course takes you much further.</p>

<h4>Week 1: Descriptive statistics</h4>
<p>Measures of central tendency (mean, median, mode) and when each is appropriate. Measures of spread: variance, standard deviation, IQR. Skewness and kurtosis. Box plots, histograms, and Q-Q plots. The difference between a population and a sample. All concepts are applied to real datasets.</p>

<h4>Week 2: Probability theory</h4>
<p>Sample spaces and events. The three axioms of probability. Conditional probability and independence. The multiplication and addition rules. Bayes' theorem — one of the most important equations in all of science. Worked examples: medical testing, spam filtering, the Monty Hall problem.</p>

<h4>Week 3: Probability distributions</h4>
<p>Discrete distributions: Bernoulli, Binomial, Poisson. Continuous distributions: Uniform, Normal (and why it's everywhere via the CLT), Exponential, Student's t. Reading and using distribution tables. Fitting distributions to real data.</p>

<h4>Week 4: Hypothesis testing</h4>
<p>The logic of statistical inference. Null and alternative hypotheses. p-values — what they actually mean and the many ways they're misunderstood. Type I and Type II errors, statistical power, and sample size calculation. One-sample, two-sample, and paired t-tests. Chi-squared tests for categorical data. ANOVA for comparing multiple groups.</p>

<h4>Week 5: Bayesian inference</h4>
<p>The Bayesian framework: prior, likelihood, posterior. Conjugate priors. Credible intervals vs confidence intervals. Bayesian A/B testing. Markov Chain Monte Carlo (MCMC) — the idea, not the full maths. Why Bayesian methods are becoming dominant in machine learning and science.</p>

<h4>Weeks 6–7: Regression and applications</h4>
<p>Simple and multiple linear regression. Assumptions and diagnostics. Logistic regression for binary outcomes. Correlation vs causation and the hazards of observational data. Putting it all together: a capstone analysis of a real dataset using everything learned in the course.</p>
""",
},

"Django & REST APIs": {
"what_you_learn": [
    "Build production-grade Django web applications using MVT architecture",
    "Design and query complex database schemas using Django ORM",
    "Build fully documented REST APIs with Django REST Framework",
    "Implement token and session authentication including JWT",
    "Write comprehensive test suites with pytest-django",
    "Deploy Django apps to a Linux server with Nginx and Gunicorn",
],
"requirements": [
    "Python proficiency (classes, decorators, context managers)",
    "Basic SQL knowledge",
    "Understanding of how HTTP and REST APIs work",
    "PostgreSQL installed locally (or Docker)",
],
"overview": """
<p>Django is the web framework that powers Instagram, Pinterest, Disqus, and The Washington Times. It follows the "batteries included" philosophy — authentication, admin panel, ORM, forms, caching, and internationalisation all come built in. When combined with Django REST Framework (DRF), it becomes one of the most productive stacks for building APIs.</p>

<h4>Weeks 1–2: Django fundamentals</h4>
<p>The MVT (Model-View-Template) pattern versus MVC. Project and app structure. URL routing and namespacing. Class-based views vs function-based views — when to use each. The template language: template inheritance, filters, tags, and context processors. The Django admin — customising list displays, search, filters, and inline models.</p>

<h4>Week 3: Models and ORM</h4>
<p>Defining models and migrations. Field types and options. QuerySets: filtering, excluding, annotating, aggregating. select_related and prefetch_related to avoid N+1 queries. Custom model managers. Signals. Working with PostgreSQL-specific features through Django.</p>

<h4>Week 4: Views, forms, and authentication</h4>
<p>Django's form system: ModelForms, validation, CSRF protection. File uploads. Django's built-in authentication: login, logout, password reset, and the User model. Extending the user model with AbstractUser. Permissions and groups.</p>

<h4>Week 5: Django REST Framework</h4>
<p>Serializers: ModelSerializer, nested serializers, custom fields and validation. Generic views and ViewSets. Routers for automatic URL generation. Browsable API. The DRF request/response cycle and how it differs from Django's.</p>

<h4>Week 6: Authentication and permissions</h4>
<p>Session authentication for browser clients. Token authentication. JWT with djangorestframework-simplejwt: access and refresh tokens, token blacklisting. Custom permission classes. Object-level permissions. Throttling.</p>

<h4>Week 7: Filtering, search, and pagination</h4>
<p>django-filter for complex filtering. Full-text search with PostgreSQL. Ordering and pagination (PageNumberPagination, CursorPagination). API versioning strategies.</p>

<h4>Weeks 8–9: Testing and deployment</h4>
<p>pytest-django: fixtures, factories with factory_boy, testing API endpoints with APITestCase and APIClient. Coverage reports. Gunicorn as WSGI server. Nginx as reverse proxy. Environment variables and secrets management. Static files with WhiteNoise. Database backups. Capstone: build and deploy a complete social API.</p>
""",
},

"Data Structures & Algorithms": {
"what_you_learn": [
    "Analyse algorithm complexity using Big O notation",
    "Implement and use arrays, linked lists, stacks, queues, heaps, and hash tables",
    "Traverse and manipulate trees and graphs with BFS and DFS",
    "Apply dynamic programming to solve problems that seem intractable",
    "Implement and compare sorting and searching algorithms",
    "Solve LeetCode-style problems confidently under time pressure",
],
"requirements": [
    "Proficiency in at least one programming language (Python used in this course)",
    "Basic understanding of functions and recursion",
    "Mathematical maturity at the level of high-school algebra",
    "Hunger — this is a challenging course and requires consistent practice",
],
"overview": """
<p>Data structures and algorithms are the foundation of computer science and the subject of the technical interview at Google, Meta, Amazon, Apple, Microsoft, and virtually every serious technology company. More than that, understanding them makes you a better programmer every day — you write code that actually scales.</p>

<p>This course is challenging. It's designed for people who are serious about getting good. We don't skip the hard problems, and we don't hide behind magic. Every data structure is implemented from scratch in Python so you understand exactly what's happening under the hood.</p>

<h4>Week 1: Arrays, strings, and complexity</h4>
<p>Big O notation: time and space complexity, best/average/worst cases, amortised analysis. Python lists as dynamic arrays. Two-pointer and sliding window patterns — two of the most powerful and reusable techniques in competitive programming. Problems: two sum, maximum subarray, minimum window substring.</p>

<h4>Week 2: Linked lists, stacks, and queues</h4>
<p>Singly and doubly linked lists: implementation, traversal, reversal, cycle detection (Floyd's algorithm). Stacks: implementing with arrays and linked lists, monotonic stack pattern. Queues and deques: circular buffer implementation. Problems: valid parentheses, daily temperatures, sliding window maximum.</p>

<h4>Week 3: Trees and heaps</h4>
<p>Binary trees: traversal (inorder, preorder, postorder, level-order), height, diameter. Binary search trees: insertion, deletion, search, BST validation. Heaps: min-heap and max-heap, heapify, the heap property. Priority queues. Problems: lowest common ancestor, kth largest element, merge k sorted lists.</p>

<h4>Week 4: Graphs</h4>
<p>Graph representations: adjacency list and matrix. BFS and DFS — the two algorithms that solve most graph problems. Topological sort (Kahn's algorithm and DFS). Union-Find (Disjoint Set Union). Shortest paths: Dijkstra's and Bellman-Ford. Problems: number of islands, course schedule, word ladder.</p>

<h4>Week 5: Sorting and searching</h4>
<p>Bubble, selection, insertion (when they're actually useful). Merge sort and its space cost. Quicksort and partition schemes. Heap sort. Counting sort, radix sort (when O(n) is achievable). Binary search and its many disguises: search in rotated array, find peak element, search in 2D matrix.</p>

<h4>Week 6: Dynamic programming</h4>
<p>The DP mindset: overlapping subproblems and optimal substructure. Top-down memoisation vs bottom-up tabulation. Classic problems: Fibonacci, climbing stairs, coin change, longest common subsequence, 0/1 knapsack, edit distance. Recognising DP problems in interviews.</p>

<h4>Weeks 7–8: Advanced topics</h4>
<p>Greedy algorithms and when they work (interval scheduling, Huffman coding). Advanced graph algorithms: minimum spanning trees (Prim's, Kruskal's), strongly connected components (Tarjan's). Tries for string problems. Segment trees for range queries.</p>

<h4>Weeks 9–10: System design and mock interviews</h4>
<p>Translating algorithmic thinking to system design: consistent hashing, bloom filters, B-trees in databases, LRU caches. How to approach and communicate during a coding interview. Ten full mock interview sessions with model solutions and common mistakes.</p>
""",
},
}
