from setuptools import setup

setup(
    name='permutable_nlp_model_inference',
    version='0.1.0',    
    description='A package for local inference of permutable nlp models',
    url='https://github.com/shuds13/pyexample',
    author='Joshua Ellis',
    author_email='joshua@permutable.ai',
    packages=['permutable_nlp_model_inference'],
    install_requires=['transformers==3.0.2',
                      'torch==1.12.1', 
                      'pandas==1.3.4'            
                      ],

    classifiers=[
        'Programming Language :: Python :: 3.8',
    ],
)
