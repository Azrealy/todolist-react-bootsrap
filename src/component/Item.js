import React, { Component}  from 'react';

class Item extends Component {
    constructor(props) {
        super(props);
        this.state = {
            isUpdated: true,
            inputValue: this.props.name
        }
    }
    handleDelete () {
        this.props.deleteTask(this.props.taskId)
    }
    handleComplete () {
        this.props.completeTask(this.props.taskId)
    }
    handleEdit () {
        this.setState ({
            isUpdated: false
        })
    }
    handleChange (event) {
        this.setState({
            inputValue: event.target.value
        })
    }
    handleUpdate () {
        this.props.updateTask(this.props.taskId, this.state.inputValue)
        this.setState({
            isUpdated: true
        })
    }
    handleCancel() {
        this.setState({ isUpdated: true, inputValue: this.props.name })
    }
    showTask() {
        var {name, isCompleted} = this.props;
        var text = '';
        var button = '';
        if (isCompleted) {
            text =  <p className='card-text'> 
                        <s onClick={this.handleEdit.bind(this)}>{name}</s>
                    </p>
        } else {
            text = 
                <p className='card-text'>
                    <b onClick={this.handleEdit.bind(this)}>{name}</b>
                </p>
        }
        if (this.state.isUpdated) {
            button = <span> 
                        <button 
                            type="button"
                            className="btn btn-sm btn-outline-secondary"
                            onClick={this.handleDelete.bind(this)}
                        >Delete</button>
                        <button 
                            type="button" 
                            className="btn btn-sm btn-outline-secondary"
                            onClick={this.handleComplete.bind(this)}
                        >Completed</button>
                    </span>
            } else {
                text = <p className='card-text'>
                            <textarea type="text" value={this.state.inputValue} onChange={this.handleChange.bind(this)}/>
                            &nbsp;&nbsp;
                       </p>
                button = 
                    <span>
                        <button 
                            type="button"
                            className="btn btn-sm btn-outline-secondary"
                            onClick={this.handleUpdate.bind(this)}
                        >Update</button>
                        <button 
                            type="button" 
                            className="btn btn-sm btn-outline-secondary"
                            onClick={this.handleCancel.bind(this)}
                        >Cancel</button>
                    </span>
            }

        return (
                <div className='card-body'>
                        {text}
                    <div className="d-flex justify-content-between ">
                        <div className="btn-group">
                            {button}
                        </div>
                    </div>
                </div>
        )
    }

    
    render () {
        return (
            <div className='col-md-4'>
                <div className='card mb-4 box-shadow'>
                    {this.showTask()}
                </div>
            </div>
        )
    };
}

export default Item