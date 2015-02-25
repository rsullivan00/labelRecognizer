class MyNode{

	private:

		unsigned xCoordinate;
		unsigned yCoordinate;

		MyNode* nextNode;

	public:

		MyNode(unsigned x = 0, unsigned y = 0, MyNode* next = NULL);
		unsigned getX();
		unsigned getY();
		MyNode* getNext();
		void setX(unsigned x);
		void setY(unsigned y);
		void setNext(MyNode* next);
};

class MyQueue{

	MyNode* head;
	MyNode* tail;

	public:

		MyQueue();
		~MyQueue();
		void pushNode(unsigned x, unsigned y);
		void popNode();
		MyNode* returnHead();
};

MyNode::MyNode(unsigned x, unsigned y, MyNode* next){

	xCoordinate = x;
	yCoordinate = y;
	nextNode = next;
}

unsigned MyNode::getX(){

	return xCoordinate;
}

unsigned MyNode::getY(){

	return yCoordinate;
}

MyNode* MyNode::getNext(){

	return nextNode;
}

void MyNode::setX(unsigned x){

	xCoordinate = x;

	return;
}

void MyNode::setY(unsigned y){

	yCoordinate = y;

	return;
}

void MyNode::setNext(MyNode* next){

	nextNode = next;

	return;
}

MyQueue::MyQueue(){

	head = NULL;
	tail = NULL;
}

MyQueue::~MyQueue(){

	while(head != NULL){

		popNode();
	}
}

void MyQueue::pushNode(unsigned x, unsigned y){

	MyNode* newNode = new MyNode(x, y);

	if(head == NULL){

		head = newNode;
		tail = head;
	}
	else{

		tail->setNext(newNode);
		tail = newNode;
	}

	return;
}

void MyQueue::popNode(){

	MyNode* temp = head;

	if(head == NULL){

		//std::cout << "Queue is empty" << std::endl;
	}
	else if(head->getNext() == NULL){

		//std::cout << head->getX() << " " << head->getY() << std::endl;

		head = NULL;
		tail = NULL;

		delete temp;
	}
	else{

		//std::cout << head->getX() << " " << head->getY() << std::endl;

		head = head->getNext();

		delete temp;
	}

	return;
}

MyNode* MyQueue::returnHead(){

	return head;
}
