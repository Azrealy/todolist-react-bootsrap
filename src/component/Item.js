import React, { Component}  from 'react';

class Item extends Component {
    constructor(props) {
        super(props);
        this.state = {
            isEdited: true
        }
    }
    handleDelete () {
        this.props.deleteTask(this.props.taskId)
    }
    handleComplete () {
        this.props.completeTask(this.props.taskId)
    }
    showTask() {
        var {name, isCompleted} = this.props;
        var operation = '';
        if (isCompleted) {
            operation = <s>{name}</s>
        } else {
            operation = 
            <span>
                <b>{name}</b>
            </span>
        }

        return (
            <div className='col-md-4'>
                <div className='card mb-4 box-shadow'>
                    <div className='card-body'>
                        <p className='card-text'>
                            {operation}
                        </p>
                        <div className="d-flex justify-content-between ">
                            <div className="btn-group">
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
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        )
    }

    
    render () {
        return (
            this.showTask()
        )
    };
}

export default Item