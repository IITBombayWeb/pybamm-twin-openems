package io.openems.edge.meter.simulated;

import org.osgi.service.cm.ConfigurationAdmin;
import org.osgi.service.component.ComponentContext;
import org.osgi.service.component.annotations.Activate;
import org.osgi.service.component.annotations.Component;
import org.osgi.service.component.annotations.ConfigurationPolicy;
import org.osgi.service.component.annotations.Deactivate;
import org.osgi.service.component.annotations.Reference;
import org.osgi.service.component.annotations.ReferenceCardinality;
import org.osgi.service.component.annotations.ReferencePolicy;
import org.osgi.service.component.annotations.ReferencePolicyOption;
import org.osgi.service.metatype.annotations.Designate;

import io.openems.common.exceptions.OpenemsException;
import io.openems.edge.bridge.modbus.api.AbstractOpenemsModbusComponent;
import io.openems.edge.bridge.modbus.api.BridgeModbus;
import io.openems.edge.bridge.modbus.api.ModbusComponent;
import io.openems.edge.bridge.modbus.api.ModbusProtocol;
import io.openems.edge.bridge.modbus.api.element.SignedWordElement;
import io.openems.edge.bridge.modbus.api.task.FC3ReadRegistersTask;
import io.openems.edge.common.component.OpenemsComponent;
import io.openems.edge.common.taskmanager.Priority;
import io.openems.edge.meter.api.ElectricityMeter;
import io.openems.edge.meter.api.MeterType;

@Designate(ocd = Config.class, factory = true) 
@Component(
		name = "Meter.Simulated", 
		immediate = true, 
		configurationPolicy = ConfigurationPolicy.REQUIRE 
)
public class MeterSimulatedImpl extends AbstractOpenemsModbusComponent 
		implements MeterSimulated, ElectricityMeter, OpenemsComponent, ModbusComponent { 

	@Reference
	private ConfigurationAdmin cm; 

	@Reference(policy = ReferencePolicy.STATIC, policyOption = ReferencePolicyOption.GREEDY, cardinality = ReferenceCardinality.MANDATORY)
	protected void setModbus(BridgeModbus modbus) {
		super.setModbus(modbus); 
	}

	private Config config = null;

	public MeterSimulatedImpl() {
		super(
				OpenemsComponent.ChannelId.values(), //
				ElectricityMeter.ChannelId.values(), //
				ModbusComponent.ChannelId.values(), //
				MeterSimulated.ChannelId.values() //
		);
	}

	@Activate
	private void activate(ComponentContext context, Config config) throws OpenemsException { 
		System.out.println("Activate called. Setting config.");
		this.config = config;
		
		if (super.activate(context, config.id(), config.alias(), config.enabled(), config.modbusUnitId(), this.cm,
				"Modbus", config.modbus_id())) {
			return;
		}
	}

	@Override
	@Deactivate
	protected void deactivate() { 
		super.deactivate();
	}

	@Override
	protected ModbusProtocol defineModbusProtocol() throws OpenemsException { 
		if (this.config == null) {
			throw new OpenemsException("Configuration is not initialized.");
		}
		
		System.out.println("DefineModbusProtocol called. Config is initialized.");

		int registerAddress = 0; 
		MeterType metertype = this.config.type();
		switch (metertype) {
			case PRODUCTION:
				registerAddress = 1000; 
				break;
			case PRODUCTION_AND_CONSUMPTION:
				registerAddress = 1001; 
				break;
			default:
				registerAddress = 1001; 
				break;
		}
		
		return new ModbusProtocol(this, 
				new FC3ReadRegistersTask(registerAddress, Priority.HIGH, 
						m(ElectricityMeter.ChannelId.ACTIVE_POWER, new SignedWordElement(registerAddress)))); 
	}

	@Override
	public MeterType getMeterType() { 
		return this.config.type();
	}

	@Override
	public String debugLog() { 
		return "L:" + this.getActivePower().asString();
	}
}
