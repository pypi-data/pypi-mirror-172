import React from 'react';
import Tab from 'react-bootstrap/Tab';
import Tabs from 'react-bootstrap/Tabs';
import Table from 'react-bootstrap/Table';

import { getObjectList, readObject } from '../../../handler';
import { CodeMirrorComponent } from '../../../common/CodeMirror';
import { DetailComponent } from '../../../common/Detail';

type DeploymentProps = {
  clickItem: Function;
  objectName: string;
};

type DeploymentState = {
  items: any[];
  currentItem: any;
};

type DeploymentObject = {
  metadata: any;
  spec: any;
  status: any;
};

class DeploymentComponent extends React.Component<
  DeploymentProps,
  DeploymentState
> {
  child: React.RefObject<DetailComponent>;
  objectName: string;

  constructor(prop: DeploymentProps) {
    super(prop);
    this.state = {
      items: [],
      currentItem: null
    };
    this.child = React.createRef();
    this.objectName = this.props.objectName;
    this.getItemList();
  }

  async getItemList() {
    const data = await getObjectList(this.objectName);

    if (data !== null) {
      this.setState({
        ...this.state,
        ['items']: data.items
      });
    }
  }

  async updateCurrentItem(item: any) {
    const data = await readObject(
      this.objectName,
      item.metadata.namespace,
      item.metadata.name
    );

    this.setState({
      ...this.state,
      ['currentItem']: data
    });
  }

  conditions(item: any) {
    const conditionList: string[] = [];

    item.status.conditions.forEach((condition: any) => {
      conditionList.push(condition.type);
    });

    return conditionList.join(',');
  }

  drawDetailContents(): JSX.Element {
    const detailRows = Object.keys(this.state.currentItem).map(key => {
      const values = this.state.currentItem[key];

      if (values !== null) {
        if (typeof values === 'object') {
          const innerRows = Object.keys(values).map(key => {
            return (
              <tr>
                <td>{key}</td>
                <td className="table-content">{JSON.stringify(values[key])}</td>
              </tr>
            );
          });

          return (
            <div>
              <h3>{key}</h3>
              <Table>
                <tbody>{innerRows}</tbody>
              </Table>
            </div>
          );
        } else {
          return (
            <div>
              <h3>{key}</h3>
              <p>{values}</p>
            </div>
          );
        }
      } else {
        return <div></div>;
      }
    });

    const props = {
      headers: this.state.currentItem.metadata.name,
      body: (
        <Tabs
          defaultActiveKey="detail"
          transition={false}
          id="detail-tabs"
          className="mb-3"
        >
          <Tab eventKey="detail" title="Detail">
            {detailRows}
          </Tab>
          <Tab eventKey="yaml" title="YAML">
            <CodeMirrorComponent code={this.state.currentItem} />
          </Tab>
        </Tabs>
      ),
      openModal: true,
      confirmEvent: () => {
        alert('Test!');
      }
    };

    return (
      <DetailComponent
        ref={this.child}
        headers={props.headers}
        body={props.body}
        openModal={true}
        confirmEvent={props.confirmEvent}
      />
    );
  }

  render(): JSX.Element {
    console.log(typeof this.state.items, this.state.items);
    const rows = this.state.items.map((item, index) => (
      <tr
        className="cursor-pointer"
        onClick={() => {
          this.props.clickItem(item);
          this.updateCurrentItem(item);
          this.child.current?.openModal(true);
        }}
      >
        <td>{index}</td>
        <td>{item.metadata.name}</td>
        <td>{item.metadata.namespace}</td>
        <td>
          {item.status.available_replicas} / {item.status.replicas}
        </td>
        <td>{item.spec.replicas}</td>
        <td>{item.metadata.creation_timestamp}</td>
        <td>{this.conditions(item)}</td>
      </tr>
    ));

    let detailContent;
    const drawDetailContent = this.state.currentItem !== null;

    console.log(this.state);

    if (drawDetailContent) {
      detailContent = this.drawDetailContents();
    } else {
      detailContent = null;
    }

    return (
      <div>
        <Table striped hover>
          <thead>
            <tr>
              <th>#</th>
              <th>Name</th>
              <th>Namespace</th>
              <th>Pods</th>
              <th>Replicas</th>
              <th>Age</th>
              <th>Conditions</th>
            </tr>
          </thead>
          <tbody>{rows}</tbody>
        </Table>
        {detailContent}
      </div>
    );
  }
}

export { DeploymentObject, DeploymentComponent };
