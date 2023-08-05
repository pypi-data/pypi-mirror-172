import React from 'react';
import Tab from 'react-bootstrap/Tab';
import Tabs from 'react-bootstrap/Tabs';
import Table from 'react-bootstrap/Table';

import { getGlobalObjectList, readGlobalObject } from '../../../handler';
import { CodeMirrorComponent } from '../../../common/CodeMirror';
import { DetailComponent } from '../../../common/Detail';

type PodSecurityPolicyProps = {
  clickItem: Function;
  objectName: string;
};

type PodSecurityPolicyState = {
  items: any[];
  currentItem: any;
};

type PodSecurityPolicyObject = {
  metadata: any;
  spec: any;
  status: any;
};

class PodSecurityPolicyComponent extends React.Component<
  PodSecurityPolicyProps,
  PodSecurityPolicyState
> {
  child: React.RefObject<DetailComponent>;
  objectName: string;

  constructor(prop: PodSecurityPolicyProps) {
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
    const data = await getGlobalObjectList(this.objectName);

    if (data !== null) {
      this.setState({
        ...this.state,
        ['items']: data.items
      });
    }
  }

  async updateCurrentItem(item: any) {
    const data = await readGlobalObject(this.objectName, item.metadata.name);

    this.setState({
      ...this.state,
      ['currentItem']: data
    });
  }

  volumes(item: any) {
    if (Object.prototype.hasOwnProperty.call(item.spec, 'volumes')) {
      return item.spec.volumes.join(',');
    }

    return '';
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
        <td>{item.spec.privileged ? 'true' : 'false'}</td>
        <td>{this.volumes(item)}</td>
        <td>{item.metadata.creation_timestamp}</td>
      </tr>
    ));

    let detailContent;
    const drawDetailContent = this.state.currentItem !== null;

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
              <th>Privileged</th>
              <th>Volumes</th>
              <th>Age</th>
            </tr>
          </thead>
          <tbody>{rows}</tbody>
        </Table>
        {detailContent}
      </div>
    );
  }
}

export { PodSecurityPolicyObject, PodSecurityPolicyComponent };
