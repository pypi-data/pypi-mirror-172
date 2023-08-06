from distutils.core import setup, Extension

def main():
    setup(name="c_explainer",
          version="1.0.0",
          description="Python interface for the c_explainer C library function",
          author="<your name>",
          author_email="your_email@gmail.com",
          ext_modules=[Extension( 
                        "c_explainer", 
                        ["source/solvers/CPP_CODE/src/bt_wrapper.cc", "source/solvers/CPP_CODE/src/Explainer.cc", "source/solvers/CPP_CODE/src/Tree.cc", "source/solvers/CPP_CODE/src/Node.cc"],
                        language="c++")])

if __name__ == "__main__":
    main()
