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
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

@Designate(ocd = Config.class, factory = true)
@Component(
    name = "Meter.Simulated",
    immediate = true,
    configurationPolicy = ConfigurationPolicy.REQUIRE
)
public class MeterSimulatedImpl extends AbstractOpenemsModbusComponent implements MeterSimulated, ElectricityMeter, OpenemsComponent, ModbusComponent {

    private static final Logger logger = LoggerFactory.getLogger(MeterSimulatedImpl.class);

    @Reference
    private ConfigurationAdmin cm;

    @Reference(policy = ReferencePolicy.STATIC, policyOption = ReferencePolicyOption.GREEDY, cardinality = ReferenceCardinality.MANDATORY)
    protected void setModbus(BridgeModbus modbus) {
        super.setModbus(modbus);
    }

    private Config config = null;

    public MeterSimulatedImpl() {
        super(
            OpenemsComponent.ChannelId.values(),
            ElectricityMeter.ChannelId.values(),
            ModbusComponent.ChannelId.values(),
            MeterSimulated.ChannelId.values()
        );
    }

    @Activate
    private void activate(ComponentContext context, Config config) throws OpenemsException {
        this.config = config;

        if (super.activate(context, config.id(), config.alias(), config.enabled(), config.modbusUnitId(), this.cm,
                "Modbus", config.modbus_id())) {
            logger.debug("Component activated with ID: {}", config.id());
        }

        logger.info("Activated with MeterType: {}", config.type());
        logger.info("Configuration - ID: {}, Alias: {}, Enabled: {}, Modbus ID: {}, Modbus Unit ID: {}",
                config.id(), config.alias(), config.enabled(), config.modbus_id(), config.modbusUnitId());
    }

    @Override
    @Deactivate
    protected void deactivate() {
        logger.debug("Deactivating MeterSimulatedImpl...");
        super.deactivate();
    }

    @Override
    protected ModbusProtocol defineModbusProtocol() throws OpenemsException {
        int modbusAddress;

        MeterType meterType = this.config.type();
        switch (meterType) {
            case PRODUCTION:
                modbusAddress = 1000;
                logger.info("Fetching data from address 1000 for PRODUCTION.");
                break;
            case CONSUMPTION_METERED:
                modbusAddress = 1001;
                logger.info("Fetching data from address 1001 for CONSUMPTION_METERED.");
                break;
            case STORAGE_SYSTEM:
                modbusAddress = 1002;
                logger.info("Fetching data from address 1002 for STORAGE_SYSTEM.");
                break;
            default:
                modbusAddress = 1000;
                logger.error("Unsupported MeterType: {}", meterType);
                throw new OpenemsException("Unsupported MeterType: " + meterType);
        }

        return new ModbusProtocol(this,
            new FC3ReadRegistersTask(modbusAddress, Priority.HIGH,
                m(ElectricityMeter.ChannelId.ACTIVE_POWER, new SignedWordElement(modbusAddress))));
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
