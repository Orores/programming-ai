from setuptools import setup

def a():
    return ['python-dotenv','requests']

# Function to read the list of dependencies from requirements.txt
def read_requirements():
    try:
        with open('requirements.txt', 'r', encoding='utf-8') as file:
            return [line.strip() for line in file.readlines()]
    except Exception as e:
        return([])

requirements = a()
requirements2 = read_requirements()
print(type(requirements))
print(type(requirements2))

# Read long description from README.md
with open('README.md', 'r', encoding="utf-8") as file:
    long_description = file.read()

setup(
    name='AutoChatBot',
    version='1.0.13',
    description='CLI chatbot that uses togetherai or openai api',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='orores',
    author_email='orores@orores.com',
    url='http://orores.com',
    license='MIT',
    packages=['AutoChatBot'],
    package_dir={'AutoChatBot': 'AutoChatBot/'},
    package_data={
        "AutoChatBot": ["context_prompts/*"]
    },
    include_package_data = True,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI approved :: MIT License',
        'Operating System :: POSIX :: Linux',
    ],
    entry_points={
        'console_scripts': ['AutoChatBot=AutoChatBot.AutoChatBot:main']
    },
    keywords='chatbot',
    python_requires=">=3.6",
    setup_requires=['wheel'],
    #install_requires=read_requirements(),  # Use the read_requirements function
    install_requires=['requests','python-dotenv','stdeb'],
)
