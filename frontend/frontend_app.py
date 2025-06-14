import gradio as gr

def dummy(): return 'Hello World'

iface = gr.Interface(fn=dummy, inputs=[], outputs='text')
iface.launch()