import React, { Component}  from 'react';

import Item from './Item';


class ItemsList extends Component {

    render () {
        return (
            <div className='row'>
            {
                this.props.taskProps.map((taskProp) => {
                    return (
                        <Item
                            taskId={taskProp.id}
                            key={taskProp.id}
                            name={taskProp.name}
                            isCompleted={taskProp.isCompleted} 
                            deleteTask={this.props.deleteTask}
                            completeTask={this.props.completeTask}/>
                    )
                })
            }
            </div>
        );
    }
}

export default ItemsList