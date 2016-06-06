node {
   stage 'Checkout'

   git url: 'https://github.com/mrazf/stringer-api'

   stage 'Setup Virtualenv'

   sh 'virtualenv env'
   sh './env/bin/pip install -r requirements.txt'

   stage 'Lint'

   sh './env/bin/python fab lint'
}
