import React, { Component}  from 'react';

class InputBox extends Component {
    constructor (props) {
        super(props);
        this.state = {
            initialTask: ''
        }
    }
    handleCreate(event) {
        event.preventDefault();
  
        this.props.createTask(this.refs.createInput.value);  //passing the value into the createTask method
        this.refs.createInput.value = '';
    }
    render () {
        return (
            <form onSubmit={this.handleCreate.bind(this)} className='card p-2'> 
                <div class='input-group'>
                    <input type='text' className='form-control' placeholder='What do I need to do?' ref="createInput"/>
                    <button type='submit' className="btn btn-primary" > Add task </button>
                </div>
            </form>
        )
    }
}

export default InputBox