import React, { Component}  from 'react';
import ItemsList from './ItemsList';
import InputBox from './InputBox';

const taskProps = [
    {
        id: 1123,
        name: 'Task still in progress.',
        isCompleted: false
    },
    {
        id: 4123,
        name: 'Have finished task this afternoon.',
        isCompleted: true
    }
]

class Main extends Component {
    constructor(props) {
        super(props);
        this.state = {
            taskProps
        };
    }
    componentDidMount () {
        return fetch('task')
            .then((response) => response.json())
            .then(responseJson => {
                console.log(responseJson)
                const taskProps = this.state.taskProps
                taskProps.push({
                    id: responseJson.key,
                    name: responseJson.name,
                    isCompleted: responseJson.isCompleted
                });
                this.setState({
                    taskProps
                });
            })
            .catch((error) => {
                console.error(error);
            });
    } 
    generateId () {
        return Math.floor(Math.random() * 9000) + 1000; 
    }
    createTask(name) {
        const id = this.generateId()
        const taskProps = this.state.taskProps
        if (name==='') {
            alert('Todo input cannt be empty')
        } else {
            taskProps.push({
                id,
                name,
                isCompleted: false
            });
            this.setState({
                taskProps
            });
        }
    }
    deleteTask(taskId) {
        var taskProps = this.state.taskProps;
        taskProps = taskProps.filter(
            (taskProp) => {
                return taskProp.id !== taskId
            }
        )
        this.setState({
            taskProps
        })
    }
    completeTask(taskId) {
        var taskProps = this.state.taskProps;
        for (let i in taskProps) {
            if (taskProps[i].id === taskId) {
                taskProps[i].isCompleted = !taskProps[i].isCompleted;
                break
            };
        }
        this.setState({
            taskProps
        })
    }
    updateTask(taskId, taskName) {
        var taskProps = this.state.taskProps;
        for (let i in taskProps) {
            if (taskProps[i].id === taskId) {
                taskProps[i].name =  taskName
                break
            };
        }
        this.setState({
            taskProps
        })
    }

    render () {
     return (
        <main>
            <section>
                <div className="container">
                    <h1> Todo List</h1>
                    <InputBox 
                        createTask={this.createTask.bind(this)}
                    />
                </div>
            </section>
            <div className='ablum py-5 bg-light'>
                <div className='container'>
                    <ItemsList 
                        taskProps={this.state.taskProps} 
                        deleteTask={this.deleteTask.bind(this)}
                        completeTask={this.completeTask.bind(this)}
                        updateTask={this.updateTask.bind(this)}
                    />
                </div>
            </div>
        </main>
     )
    }
}

export default Main