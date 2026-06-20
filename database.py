from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_cors import CORS

db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()
mail = Mail()


def init_db(app):
    """Initialize all Flask extensions."""
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    with app.app_context():
        # Import models to register them
        from models.user import User
        from models.chat import ChatHistory
        from models.faq import FAQ
        from models.admin import Admin
        from models.notification import Notification

        db.create_all()
        _seed_default_data()


def _seed_default_data():
    """Seed default FAQs and admin account if not present."""
    from models.admin import Admin
    from models.faq import FAQ
    from models.notification import Notification
    from flask_bcrypt import generate_password_hash

    # Create default admin
    if not Admin.query.filter_by(username='admin').first():
        admin = Admin(
            username='admin',
            email='admin@college.edu',
            password=generate_password_hash('Admin@123').decode('utf-8')
        )
        db.session.add(admin)

    # Seed FAQs
    if FAQ.query.count() == 0:
        faqs = [
            # Admissions
            FAQ(category='Admissions', question='What is the admission process?',
                answer='The admission process involves: 1) Fill the online application form on our website. 2) Submit required documents (10th & 12th marksheets, ID proof). 3) Appear for entrance test (if applicable). 4) Attend counseling session. 5) Pay the admission fee to confirm your seat.',
                keywords='admission,apply,process,how to join,enroll', priority=10),
            FAQ(category='Admissions', question='What are the eligibility criteria for admission?',
                answer='Eligibility varies by course: For B.Tech: 60% in 10+2 with Physics, Chemistry, Math. For MBA: Graduation with 50% marks + valid CAT/MAT score. For BCA: 50% in 10+2 with Math. Contact the admissions office for specific course requirements.',
                keywords='eligibility,criteria,qualification,marks,percentage', priority=9),
            FAQ(category='Admissions', question='What is the last date for admission?',
                answer='Admissions are typically open from June to August each year. The last date for the current academic year is August 31st. Please check our official website or contact the admissions office for exact dates.',
                keywords='last date,deadline,admission date,when', priority=8),
            FAQ(category='Admissions', question='What documents are required for admission?',
                answer='Required documents: 1) 10th Marksheet & Certificate 2) 12th Marksheet & Certificate 3) Transfer Certificate 4) Migration Certificate 5) Character Certificate 6) Passport-size photographs (6) 7) Aadhar Card / ID Proof 8) Category Certificate (if applicable)',
                keywords='documents,required,certificates,papers', priority=8),

            # Fees
            FAQ(category='Fees', question='What is the fee structure?',
                answer='Fee structure for major courses: B.Tech: ₹85,000/year | MBA: ₹75,000/year | BCA: ₹45,000/year | BBA: ₹40,000/year | B.Sc: ₹35,000/year. Fees include tuition, library, lab, and sports facilities. Hostel fees are separate.',
                keywords='fee,fees,cost,charges,tuition,amount', priority=10),
            FAQ(category='Fees', question='Are there any scholarships available?',
                answer='Yes! We offer multiple scholarships: 1) Merit Scholarship (top 10% students get 25% fee waiver) 2) Government SC/ST/OBC scholarships 3) Sports quota scholarship 4) Management quota scholarship 5) Need-based financial aid. Apply through the scholarship portal.',
                keywords='scholarship,financial aid,fee waiver,discount', priority=9),
            FAQ(category='Fees', question='What are the payment modes for fees?',
                answer='Fees can be paid via: Online payment (Net Banking, UPI, Credit/Debit Card) through our student portal, Demand Draft in favor of "College Name", Cash payment at the accounts office. EMI options are available for annual fees.',
                keywords='payment,pay,online,DD,demand draft,EMI', priority=7),

            # Courses
            FAQ(category='Academics', question='What courses are offered?',
                answer='We offer: Undergraduate: B.Tech (CS, IT, ECE, ME, CE), BCA, BBA, B.Sc, B.Com, BA. Postgraduate: M.Tech, MBA, MCA, M.Sc. Diploma: Various 1-3 year diploma programs. PhD programs in select departments.',
                keywords='courses,programs,branches,departments,offered', priority=10),
            FAQ(category='Academics', question='What is the academic calendar?',
                answer='Academic Year: July to May. Semester 1: July–November | Exams: November. Semester 2: December–April | Exams: April–May. Summer internships: May–June. Results are declared within 30 days of exams.',
                keywords='academic calendar,schedule,semester,dates,timetable', priority=8),
            FAQ(category='Academics', question='What is the exam schedule?',
                answer='Mid-semester exams are held in September and February. End-semester exams are in November and April/May. Practical exams are conducted in the last week of each semester. Exact dates are published on the college website 30 days in advance.',
                keywords='exam,examination,test,schedule,dates', priority=9),

            # Hostel
            FAQ(category='Hostel', question='Is hostel facility available?',
                answer='Yes, we have separate hostels for boys and girls. Facilities include: AC and non-AC rooms, 24/7 security, Wi-Fi, mess with hygienic food, laundry, gym, common room with TV, medical facility. Hostel fee: ₹60,000–₹90,000/year (including mess).',
                keywords='hostel,accommodation,room,stay,boarding', priority=9),
            FAQ(category='Hostel', question='What are the hostel rules?',
                answer='Key hostel rules: Entry/exit timings: 6 AM – 10 PM. Visitors allowed only in designated areas on weekends. No alcohol/smoking on campus. Ragging is strictly prohibited. Mess timings: Breakfast 7-9 AM, Lunch 12-2 PM, Dinner 7-9 PM.',
                keywords='hostel rules,timing,regulations,mess', priority=7),

            # Placements
            FAQ(category='Placements', question='What is the placement record?',
                answer='Our placement statistics: 2023-24: 95% placement rate | Highest package: ₹42 LPA | Average package: ₹8.5 LPA. Top recruiters: TCS, Infosys, Wipro, Accenture, Amazon, Microsoft, Deloitte, HDFC Bank. 200+ companies visit campus annually.',
                keywords='placement,job,package,salary,recruit,company', priority=10),
            FAQ(category='Placements', question='How does the placement process work?',
                answer='Placement process: 1) Register on the placement portal. 2) Attend pre-placement training (aptitude, coding, soft skills). 3) Companies visit for campus drives. 4) Clear aptitude test → Group Discussion → Technical Interview → HR Interview. 5) Receive offer letter.',
                keywords='placement process,campus drive,interview,how', priority=8),

            # Transport
            FAQ(category='Transport', question='Is transport facility available?',
                answer='Yes, college buses operate on 15+ routes covering major areas of the city. Bus timings: Morning pickup 7:00–8:30 AM, Evening drop 4:30–6:00 PM. Bus pass fee: ₹8,000–₹12,000/year depending on distance. Contact the transport office for route details.',
                keywords='transport,bus,route,vehicle,travel', priority=8),

            # Scholarships
            FAQ(category='Scholarships', question='How to apply for scholarships?',
                answer='To apply for scholarships: 1) Visit the scholarship section on our website. 2) Check eligibility for each scholarship. 3) Fill the scholarship application form. 4) Submit required documents (income certificate, marksheets, etc.). 5) Applications are reviewed by the scholarship committee. Results announced within 45 days.',
                keywords='scholarship apply,how to apply,scholarship form', priority=9),

            # General
            FAQ(category='General', question='What are the college timings?',
                answer='College timings: Monday to Friday: 8:00 AM – 5:00 PM. Saturday: 8:00 AM – 1:00 PM. Administrative office: 9:00 AM – 5:00 PM (Mon–Sat). Library: 8:00 AM – 8:00 PM. The college remains closed on Sundays and public holidays.',
                keywords='timing,time,hours,open,close,schedule', priority=8),
            FAQ(category='General', question='What is the contact information?',
                answer='Contact us: Phone: +91-XXXXXXXXXX | Email: info@college.edu | Admissions: admissions@college.edu | Address: College Road, City - 000000. You can also visit us Monday–Saturday between 9 AM and 5 PM.',
                keywords='contact,phone,email,address,location', priority=9),
        ]
        for faq in faqs:
            db.session.add(faq)

    # Seed a welcome notification
    if Notification.query.count() == 0:
        notif = Notification(
            title='Welcome to College Chatbot',
            message='Our AI-powered chatbot is now live! Ask any question about admissions, fees, courses, and more.',
            category='general'
        )
        db.session.add(notif)

    db.session.commit()
