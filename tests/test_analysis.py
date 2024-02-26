
def test_analysis_config():
    from analysis import Analysis

    input='configs/config.yml'
    output= Analysis('configs/config.yml')
    output= output.show_config()
    expected_output= """Consolidated Configuration:
    plot: {'color': 'blue'}
    default_save_path: path
    github: {'api_token': "don't need one cause not using github_api"}
    notification: {'ntfy_topic': 'YSlYtkDXpplz4OqW'}
    visualization: {'plot_title': 'Count of Pokemon Species per Color', 'x_axis_title': 'Color', 'y_axis_title': 'Count', 'figure_size': {'width': 10, 'height': 12}}
    output: {'save_path': 'output/', 'log_path': 'output/'}"""

    assert output == expected_output, "The output does not match the expected output."
    
def test_load_data():
    from analysis import load_data
    import requests

    input='https://pokeapi.co/api/v2/pokemon/?limit=1025'
    output=load_data(input)
    output_count=output['count']
    expected_output_count=1302

    assert output_count == expected_output_count, "The count of the output data loaded does not match what is expected"


