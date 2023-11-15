const express = require('express');
const app = express();
const port = process.env.PORT || 3000;
const Cloudant = require('@cloudant/cloudant');
const { CloudantV1 } = require('@ibm-cloud/cloudant');
const { IamAuthenticator } = require('ibm-cloud-sdk-core');

// Initialize Cloudant connection with IAM authentication
async function dbCloudantConnect() {
    try {
        const cloudant = Cloudant({
            plugins: { iamauth: { iamApiKey: 'eXdat4Y8oJC_D_OBI7o_tEdAep_q8ArhgVG1aiBm4LGS' } },
            url: 'https://b7402ac4-cbd2-4519-87c7-642ac2b6b556-bluemix.cloudantnosqldb.appdomain.cloud',
        });

        const db = cloudant.use('dealerships');
        console.info('Connect success! Connected to DB');
        return db;
    } catch (err) {
        console.error('Connect failure: ' + err.message + ' for Cloudant DB');
        throw err;
    }
}

let db;

(async () => {
    db = await dbCloudantConnect();
})();

app.use(express.json());

// Define a route to get all dealerships with optional state and ID filters
app.get('/dealerships/get', (req, res) => {
    const { state, id } = req.query;

    // Create a selector object based on query parameters
    const selector = {};
    if (state) {
        selector.state = state;
    }
    
    if (id) {
        selector.id = parseInt(id); // Filter by "id" with a value of 1
    }

    const queryOptions = {
        selector,
        limit: 10, // Limit the number of documents returned to 10
    };

    db.find(queryOptions, (err, body) => {
        if (err) {
            console.error('Error fetching dealerships:', err);
            res.status(500).json({ error: 'An error occurred while fetching dealerships.' });
        } else {
            const dealerships = body.docs;
            res.json(dealerships);
        }
    });
});

app.get("/status", async (req, res) => {
      const authenticator = new IamAuthenticator({ apikey: 'eXdat4Y8oJC_D_OBI7o_tEdAep_q8ArhgVG1aiBm4LGS' })
      const cloudant = CloudantV1.newInstance({
          authenticator: authenticator
      });
      cloudant.setServiceUrl('https://b7402ac4-cbd2-4519-87c7-642ac2b6b556-bluemix.cloudantnosqldb.appdomain.cloud');
      try {
        let dbList = await cloudant.getAllDbs();
        return { "dbs": dbList.result };
      } catch (error) {
          return { error: error.description };
      }
});

app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
});