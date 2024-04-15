from librar import *

# Create a Flask application instance
app = Flask(__name__)

# Load existing experiment names from the JSON file
def load_experiment_names():
    try:
        with open("experiment_names.json", "r") as json_file:
            data = json.load(json_file)
            return data["experiment_details"]
    except FileNotFoundError:
        return []

# Save experiment names to the JSON file
def save_experiment_names(experiment_names, current_experiment):
    data = {"experiment_details": experiment_names, "current_experiment": '', 'commodity':''}
    with open("experiment_names.json", "w") as json_file:
        json.dump(data, json_file)

# -------------------
# -------------------
@app.route('/', methods=['GET'])
def home():
    # experiment_names = ["Exp1", "Exp2"]
    data = ''
    if not os.path.isfile('experiment_names.json'):
        with open("experiment_names.json", "w") as json_file:
            data = {"experiment_details": [], "current_experiment": "", "current_commodity":""}
            json.dump(data, json_file)
    else:
        with open("experiment_names.json", "r") as json_file:
            data = json.load(json_file)
        data['current_experiment'] = ''
        data['current_commodity'] = ''
        with open("experiment_names.json", "w") as json_file:
            data = {"experiment_details": data['experiment_details'], "current_experiment": "", "current_commodity":""}
            json.dump(data, json_file)

    # data1 = {"experiment_details": [{"commodity": "gold", "experiment_name": ["new1", "new2"]}]}
    return render_template('home.html', experiment_names=data['experiment_details'])

    # return jsonify({"Page_status": "home.html Successfully rendered"})


@app.route('/', methods=['POST'])
def form():
    commodity = request.form['commodity']
    experiment = request.form['experiment']
    experiment_name = None
    if experiment == 'New Experiment':
        experiment_name = request.form['new_experiment_name']
    else:
        experiment_name = request.form['existing_experiment_name']
        # Do something with existing_experiment_name if needed
    with open("experiment_names.json", "r") as json_file:
        data = json.load(json_file)
    
    first_experiment = False
    # Search for experiment details with the desired commodity
    for experiment_detail in data["experiment_details"]:
        if experiment_detail["commodity"] == commodity:
            # Get the experiment names for the desired commodity
            experiment_names = experiment_detail["experiment_name"]
            if experiment_name not in experiment_names:
                experiment_names.append(experiment_name)
            # Update the experiment_names in the JSON data
            experiment_detail["experiment_name"] = experiment_names
            break
        else:
            first_experiment = True
        
    if first_experiment == True:
        if commodity == 'Crude Oil':
            commodity = 'Crude_oil'
        dict1 = {"commodity": commodity, "experiment_name": [experiment_name]}
        data["experiment_details"].append(dict1)
    data["current_commodity"] = commodity
    data["current_experiment"] = experiment_name
    print(data)

    with open("experiment_names.json", "w") as json_file:
        json.dump(data, json_file)

    # data1 = {"experiment_details": [{"commodity": "gold", "experiment_name": ["new1", "new2"]}], ""}

    return redirect(url_for('experimentConfig'))
    # if experiment == 'New Experiment':
    #     return jsonify({
    #         "commodity": commodity,
    #         "experiment": experiment,
    #         "new_experiment_name": experiment_name,
    #         "existing_experiment_name": ""
    #     })
    # else:
    #     return jsonify({
    #         "commodity": commodity,
    #         "experiment": experiment,
    #         "new_experiment_name": experiment_name,
    #         "existing_experiment_name": experiment_name,
    #     })

@app.route('/experiment_names', methods=['POST'])
def get_experiment_names():
    selected_commodity = request.form['commodity']
    with open("experiment_names.json", "r") as json_file:
        data = json.load(json_file)
    experiment_names_filtered = []
    for experiment_detail in data["experiment_details"]:
        if experiment_detail["commodity"] == selected_commodity:
            # Get the experiment names for the desired commodity
            experiment_names_filtered = experiment_detail["experiment_name"]
            break
    return jsonify({'commodity':selected_commodity,'experiment_names_filtered':experiment_names_filtered})
    
## --------------------
## --------------------
@app.route('/ExperimentConfiguration', methods=['GET'])
def experimentConfig():
    with open("experiment_names.json", "r") as json_file:
        data = json.load(json_file)
    # need to add current experiment and pass it to render_template below
    return render_template('experimentConfig.html', experiment=data['experiment_details'])
    # return jsonify({
    #     "page_status": "experimentConfig.html Successfully Rendered"
    # })

@app.route('/ExperimentConfiguration/upload', methods=['POST'])
def upload_file():
    if 'myfile' not in request.files:
        return "No file part"
    
    file = request.files['myfile']
    print(file)
    
    if file.filename == '':
        return "No selected file"
    os.makedirs('uploaded_files', exist_ok=True)
    # Save file to uploaded_files folder
    file.save(os.path.join('uploaded_files', file.filename))
    
    # return jsonify({'message': 'File uploaded successfully'})
    return '', 204

@app.route('/experimentConfiguration', methods=['POST'])
def experimentSubmit():
    granularity = request.form['granularity']
    horizon = request.form['forecasthorizon']
    granularity_level = request.form['granularity_level']
    # horizon_level = request.form['horizon_level']
    lookback = request.form['lookback']
    lookahead = request.form['lookahead']
    # lookback_level = request.form['lookback_level']

    # print(granularity, horizon, horizon_level, lookback_level, lookback_level)
    return redirect(url_for('getTransformations'))
    # return jsonify({
    #     'granularity': granularity,
    #     'forecasthorizon': granularity_level,
    #     'lookback':lookback,
    #     'lookahead': lookahead
    # })

# -------------------------
# -------------------------
def plotPDFSC3(df1):
    fig_pdf = px.histogram(df1, x="Price", marginal="rug", 
                       title='Probability Density Function (PDF)',
                       labels={'Price': 'Price', 'y': 'Density'})
    return fig_pdf

def plotCDFSC3(df1):
    fig_cdf = px.histogram(df1, x="Price", cumulative=True, histnorm='probability', nbins=20, 
                       title='Cumulative Distribution Function (CDF)',
                       labels={'Price': 'Price', 'y': 'Probability'})
    return fig_cdf

def plotBoxSC3(df1):
    fig_box = px.box(df1, y="Price", 
                 title='Box Plot of Prices',
                 labels={'Price': 'Price'})
    return fig_box

def plotHistogramSC3(df1):
    fig_hist = px.histogram(df1, x="Price", 
                        title='Histogram of Prices',
                        labels={'Price': 'Price', 'y': 'Count'})
    return fig_hist

def plotScatterSC3(df1):
    fig_scatter = px.scatter(df1, x='DATE', y='Price', 
                         title='Scatter Plot of Prices',
                         labels={'DATE': 'Date', 'Price': 'Price'})
    return fig_scatter

def plotLineSC3(df1):
    fig_line = px.line(df1, x='DATE', y='Price', 
                   title='Line Plot of Prices',
                   labels={'DATE': 'Date', 'Price': 'Price'})
    return fig_line

# @app.route('/getS3Plot', methods=['POST'])
# def getScreen3Plot():
#     filenames = os.listdir('uploaded_files')
#     csv_filename = [filename for filename in filenames if filename.endswith('.csv')][0]
#     df1 = pd.read_csv(f'uploaded_files/Aluminium_dataset_csv_tj.csv')
#     plot = request.form['plotselected']
#     list = {"PDF":plotPDFSC3(df1).to_html(''),"CDF": plotCDFSC3(df1).to_html(''),"BoxPlot": plotBoxSC3(df1).to_html(''),
#             "LineChart": plotLineSC3(df1).to_html(''),"Scatter": plotScatterSC3(df1).to_html(''), "Histogram": plotHistogramSC3(df1).to_html('')}
    
#     # return list[plot]
#     return Response(list[plot], mimetype='text/plain')


@app.route('/transformations', methods=['GET'])
def getTransformations():
    filenames = os.listdir('uploaded_files')
    csv_filename = [filename for filename in filenames if filename.endswith('.csv')][0]
    df1 = pd.read_csv(f'uploaded_files/Aluminium_dataset_csv_tj.csv')
    column_names = df1.columns
    # nan_indices = df1[df1['Price'].isnull()].index
    # fig_pdf = plotPDFSC3(df1)
    # list = {}
    

    return render_template('transformations.html', pdf_fig=plotPDFSC3(df1).to_html(''),cdf_fig= plotCDFSC3(df1).to_html(''),box_fig= plotBoxSC3(df1).to_html(''),
            line_fig= plotLineSC3(df1).to_html(''),scatter_fig= plotScatterSC3(df1).to_html(''), hist_fig= plotHistogramSC3(df1).to_html(''))
    # return jsonify({
    #     'page_status': "Transformations.html Successfully Loaded"
    # })


@app.route('/transformations', methods=['POST'])
def submitVisuals():

    return redirect(url_for('scheduleExperiment'))

    # return jsonify({'page_status': "Transformations.html successfully loaded"})

# -------------------------
# -------------------------
@app.route('/scheduleExperiment', methods=['GET'])
def scheduleExperiment():
    # need to add current experiment and pass it to render_template below
    return render_template('scheduleExp.html')
    # return jsonify({'page_status': "scheduleExperiment.html successfully loaded"})

@app.route('/scheduleExperiment', methods=['POST'])
def trainModel():
    algorithms_selected = request.form.getlist('algorithmsselected')
    selectedfeatures = request.form.getlist('selectedfeatures')
    data = {"selected_algorithms": algorithms_selected, "selected_features": selectedfeatures}
    with open("training_data.json", "w") as json_file:
        data = json.dump(data,json_file)

    # need to add current experiment and pass it to render_template below
    return redirect(url_for('resultsAndDashboard'))

    # return jsonify({
    #     'algorithmsselected':algorithms_selected,
    #     'selectedfeatures': selectedfeatures,
    # })

# -------------------------
# -------------------------

def plotModels(modelName):
    print("Hello awesome")
    directory = 'data/'
    filenames = os.listdir(directory)
    csv_filenames = [filename for filename in filenames if filename.endswith('.csv')]
    # Print the list of CSV filenames
    print("CSV Files in the directory:")
    current_file = ''
    with open("experiment_names.json", "r") as json_file:
        data = json.load(json_file)
    print(data)
    for filename in csv_filenames:
        if data['current_commodity'].lower() in filename.lower(): 
            current_file = filename
    print(current_file)
    df1 = pd.read_csv(f"data/{current_file}")
    print(df1.head())
    # df1 = df1.rename(columns={'ALUMINUM': 'ALUMINIUM'})
    # Create traces
    traces = []
    print(modelName)
    traces.append(go.Scatter(x=df1['DATE'], y=df1['Price'], mode='lines', name='Actual Price'))

    traces.append(go.Scatter(x=df1['DATE'], y=df1[modelName], mode='lines', name=modelName))
    print(traces)
    # for column in df1.columns[1:]:
    #     traces.append(go.Scatter(x=df1['DATE'], y=df1[column], mode='lines', name=column))
    current_commodity = data['current_commodity']
    # Create layout
    layout = go.Layout(
        title=f'Predicted Price of {current_commodity}',
        xaxis=dict(title='Date'),
        yaxis=dict(title=modelName)
    )

    # Create figure
    fig = go.Figure(data=traces, layout=layout)

    return fig

@app.route('/results', methods=['GET'])
def resultsAndDashboard():
    with open("training_data.json", "r") as json_file:
        data = json.load(json_file)
    models = data['selected_algorithms']
    return render_template('results.html', models=models)

    # return jsonify({
    #     'page_status': "results.html is loaded"
    # })

@app.route('/results', methods=['POST'])
def submitModel():
    modelName = request.form['modelselected']
    with open("training_data.json", "r") as json_file:
        data = json.load(json_file)
    models = data['selected_algorithms']
    fig = plotModels(modelName)
    print("hello")

    # If content type is not JSON, render the template
    return render_template('results.html', modelname=modelName, fig=fig.to_html(), models=models)
    # return jsonify({
    #     'modelselected': modelName
    # })
# Run the app
if __name__ == '__main__':
    app.run(port=8000,debug=True)
