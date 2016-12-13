import random
import string
import datetime

first_names = [
"James", "John", "Robert", "Michael", "William", "David", "Richard", "Joseph", "Thomas",
"Charles", "Christopher", "Daniel", "Matthew", "Anthony", "Donald", "Mark", "Paul",
"Steven", "George", "Kenneth", "Andrew", "Joshua", "Edward", "Brian", "Kevin", "Ronald",
"Timothy", "Jason", "Jeffrey", "Ryan", "Gary", "Jacob", "Nicholas", "Eric", "Stephen",
"Jonathan", "Larry", "Scott", "Frank", "Justin", "Brandon", "Raymond", "Gregory", "Samuel",
"Benjamin", "Patrick", "Jack", "Alexander", "Dennis", "Jerry", "Tyler", "Aaron", "Henry", "Douglas",
"Peter", "Jose", "Adam", "Zachary", "Walter", "Nathan", "Harold", "Kyle", "Carl", "Arthur", "Gerald",
"Roger", "Keith", "Jeremy", "Lawrence", "Terry", "Sean", "Albert", "Joe", "Christian", "Austin",
"Willie", "Jesse", "Ethan", "Billy", "Bruce", "Bryan", "Ralph", "Roy", "Jordan", "Eugene", "Wayne",
"Louis", "Dylan", "Alan", "Juan", "Noah", "Russell", "Harry", "Randy", "Philip", "Vincent",
"Gabriel", "Bobby", "Johnny", "Howard"
"Mary", "Patricia", "Jennifer", "Elizabeth", "Linda", "Barbara", "Susan", "Jessica", "Margaret", "Sarah",
"Karen", "Nancy", "Betty", "Dorothy", "Lisa", "Sandra", "Ashley", "Kimberly", "Donna", "Carol",
"Michelle", "Emily", "Helen", "Amanda", "Melissa", "Deborah", "Stephanie", "Laura", "Rebecca",
"Sharon", "Cynthia", "Kathleen", "Shirley", "Amy", "Anna", "Angela", "Ruth", "Brenda", "Pamela",
"Virginia", "Katherine", "Nicole", "Catherine", "Christine", "Samantha", "Debra", "Janet", "Carolyn",
"Rachel", "Heather", "Maria", "Diane", "Emma", "Julie", "Joyce", "Frances", "Evelyn", "Joan", "Christina",
"Kelly", "Martha", "Lauren", "Victoria", "Judith", "Cheryl", "Megan", "Alice", "Ann", "Jean",
"Doris", "Andrea", "Marie", "Kathryn", "Jacqueline", "Gloria", "Teresa", "Hannah", "Sara", "Janice",
"Julia", "Olivia", "Grace", "Rose", "Theresa", "Judy", "Beverly", "Denise", "Marilyn", "Amber",
"Danielle", "Brittany", "Madison", "Diana", "Jane", "Lori", "Mildred", "Tiffany", "Natalie", "Abigail",
"Kathy"
]

family_names = [
"SMITH", "JOHNSON", "WILLIAMS", "JONES", "BROWN", "DAVIS", "MILLER", "WILSON", "MOORE",
"TAYLOR", "ANDERSON", "THOMAS", "JACKSON", "WHITE", "HARRIS", "MARTIN", "THOMPSON", "GARCIA",
"MARTINEZ", "ROBINSON", "CLARK", "RODRIGUEZ", "LEWIS", "LEE", "WALKER", "HALL", "ALLEN",
"YOUNG", "HERNANDEZ", "KING", "WRIGHT", "LOPEZ", "HILL", "SCOTT", "GREEN", "ADAMS", "BAKER",
"GONZALEZ", "NELSON", "CARTER", "MITCHELL", "PEREZ", "ROBERTS", "TURNER", "PHILLIPS", "CAMPBELL",
"PARKER", "EVANS", "EDWARDS", "COLLINS", "STEWART", "SANCHEZ", "MORRIS", "ROGERS", "REED",
"COOK", "MORGAN", "BELL", "MURPHY", "BAILEY", "RIVERA", "COOPER", "RICHARDSON", "COX",
"HOWARD", "WARD", "TORRES", "PETERSON", "GRAY", "RAMIREZ", "JAMES", "WATSON", "BROOKS", "KELLY",
"SANDERS", "PRICE", "BENNETT", "WOOD", "BARNES", "ROSS", "HENDERSON", "COLEMAN", "JENKINS",
"PERRY", "POWELL", "LONG", "PATTERSON", "HUGHES", "FLORES", "WASHINGTON", "BUTLER", "SIMMONS",
"FOSTER", "GONZALES", "BRYANT", "ALEXANDER", "RUSSELL", "GRIFFIN", "DIAZ", "HAYES"
]

email_domains = ['email.hu', 'mail.com', 'messenger.org', 'univ.edu', 'contact.net']

class UserGenerator(object):
    """Generate user data"""

    def generate_first_name(self):
        return random.choice(first_names)

    def generate_family_name(self):
        return random.choice(family_names).capitalize()

    def generate_birth_date(self):
        year = random.randint(1940, 2000)
        month = random.randint(1, 12)
        day = random.randint(1, 28)
        return datetime.date(year, month, day)

    def generate_email(self, first_name, family_name):
        first = first_name.lower()
        family = family_name.lower()
        email = ''
        if random.choice([True, False]):
            email = email + first
        else:
            email = ''.join(random.sample(string.ascii_lowercase, random.randint(4, 10)))
        if random.choice([True, False]):
            email = email + random.choice(['', '.', '-', '_'])
            email = email + family
        if random.choice([True, False]):
            email = email + random.choice(['', '.', '-', '_'])
            email = email + str(random.randint(1, 1000))
        if email == '':
            email = ''.join(random.sample(string.ascii_lowercase, random.randint(4, 10)))
        email += '.' + random.choice(email_domains)
        return email

    def generate_password(self):
        return random.sample(string.ascii_letters, random.randint(6, 12))
