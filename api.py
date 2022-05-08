import json
from flask import Flask, request
from jobs import add_job

app = Flask(__name__)

  @app.route('/jobs/<substance>', methods=['POST'])
  def jobs_api(substance):
        """
        application route to create new job. This route accepts a JSON payload
        describing the job to be created.
        :param: substance
        """
        return add_job(str(substance))


  if __name__ == '__main__':
      app.run(debug=True, host='0.0.0.0')
